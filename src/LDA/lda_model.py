"""
Title: lda_model.py

Description:
    This file contains the classes
    TopicModel, TopicList and WordList.
    THe TopicModel class can be used
    to apply LDA topic modelling to the dataset
    in parquet format.

Author:
    Konrad Brüggemann,
    Universität Potsdam,
    brueggemann4@uni-potsdam.de

Date:
    05.07.2024

Usage:
    Pass the processed speeches.parquet file to the
    TopicModel class, and run the file using\n
    python -m src/LDA/topic_model.py --filename [filename]
"""

import argparse
import json
import logging
import os
import re
from datetime import datetime
from typing import Literal

import gensim
import polars as pl
import pyLDAvis
import pyLDAvis.gensim_models
import spacy
from gensim.corpora import Dictionary
from gensim.models import LdaModel, LsiModel, HdpModel
from nltk.corpus import stopwords
from spacy.tokens import Doc
from tqdm import tqdm

from src.LDA.exceptions import EmptyCorpusError
from src.LDA.topic_naming import Topic

logger = logging.getLogger(__name__)
Doc.set_extension('custom_attr', default=True)


class TopicList:
    """
    A class to represent and process topics
    generated from a topic modeling algorithm.

    This class handles the organization of topics,
    their distribution across documents,
    and the relationship between topics and political parties.
    """

    def __init__(
            self,
            topic_word_dict: dict[int, list[str]],
            topic_distributions: list[tuple],
            parties: list[str]
    ) -> None:
        """
        Initialize the TopicList object.

        Args:
        topic_word_dict: A dictionary mapping topic IDs to words.
        topic_distributions: List of tuples with the topic distributions.
        parties: A list of parties associated with documents.
        """

        self.topic_word_dict = topic_word_dict

        self.topic_distributions = topic_distributions
        self.average_share_of_topic = self.get_accumulated_share()

        self.parties = parties
        self.topics_parties = self.get_party_topics()

    def get_accumulated_share(self) -> float:
        """
        This method computes the cumulative share of each topic
        and then averages it by the number of documents.

        Returns:
            dict[int, float]: A dictionary mapping topic IDs
            to their average share.
        """

        topic_cumulative_share = {}
        topic_counts = {}

        for document in self.topic_distributions:
            for topic_id, share in document:
                if topic_id not in topic_cumulative_share:
                    topic_cumulative_share[topic_id] = 0
                    topic_counts[topic_id] = 0
                topic_cumulative_share[topic_id] += share
                topic_counts[topic_id] += 1

        topic_average_share = {
            topic_id: topic_cumulative_share[topic_id] /
                      topic_counts[topic_id]
            for topic_id in topic_cumulative_share
        }

        return topic_average_share

    def get_party_topics(self) -> dict[int, list[str]]:
        """
        This method analyzes the topic distribution
        across documents to identify the main topic
        for each document and records which parties
        are associated with which topics.

        Returns:
            dict: A dictionary mapping topic IDs to sets of parties.
        """

        party_topics = {}
        for idx, document in enumerate(self.topic_distributions):

            party = self.parties[idx]
            main_topic = max(document, key=lambda x: x[1])[0]

            if main_topic not in party_topics:
                party_topics[main_topic] = set([party])
            else:
                party_topics[main_topic].add(party)

        print(party_topics)
        return party_topics

    def align_topics(self):
        """
        This generator method yields tuples containing
        the word list, average share of the topic,
        and associated parties for each topic.

        Yields:
            tuple: A tuple containing a WordList object,
            the average share of the topic,
            and a set of parties.
        """

        num_docs = len(self.topic_word_dict)
        for topic_id in range(0, (num_docs - 1)):
            word_list = WordList(self.topic_word_dict[str(topic_id)])
            relative_share = self.average_share_of_topic[topic_id]
            parties = self.topics_parties[topic_id]
            yield (word_list, relative_share, parties)

    def __iter__(self):
        return iter(self.align_topics())


class WordList:
    """
    A class to represent a list of words associated with a topic.

    This class provides methods to
    convert the word list to a string,
    represent it for debugging, and iterate over it.
    """

    def __init__(self, word_list: list[str]) -> None:
        self.word_list = word_list

    def __str__(self):
        """
        Return a string representation of the word list by
        joining the words in the list with a comma and a space.

        Returns:
            str: A string representation of the word list.
        """
        return ', '.join(self.word_list)

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter(self.word_list)


class TopicModel:
    """
    A class to perform topic modelling on a dataset.

    This class supports three modelling algorithms: LDA, LSI, and HDP.
    It can preprocess the dataset before modelling the topics,
    which can be deactivated using the 'process' parameter.
    """

    def __init__(
            self,
            dataset: pl.DataFrame,
            process: bool = True,
            topic_model: Literal['LDA', 'LSI', 'HDP'] = None
    ) -> None:
        """
        Initialize the TopicModel object.

        Args:
            dataset: A polars DataFrame containing the speeches.
            process: Whether to apply preprocessing to the dataset.
            topic_model: The desired topic modelling algorithm.
        """

        self.topic_model = topic_model
        self.nlp = spacy.load('de_core_news_lg')

        # german stopwords
        self.german_stop_words = stopwords.words('german')
        # add custom stopwords
        with (open('src/LDA/custom_stopwords.txt', 'r', encoding='utf-8')
              as fp):
            sw = [line.strip() for line in fp.readlines()]
            self.german_stop_words.extend(sw)

        self.factions_data = pl.read_parquet(args.filename1)

        # add year column
        dataset = dataset.with_columns(
            dataset["date"].map_elements(
                self.get_year_from_date,
                return_dtype=str).alias("year")
        )

        if process:
            self.data: pl.DataFrame = self.prepare_dataset(dataset)
        else:
            self.data: pl.DataFrame = dataset

    @property
    def word_count(self) -> int:
        """
        The number of words in the dataset.
        """
        texts = self.data.filter(pl.col('speechContent') != '')[
            'speechContent'].to_list()
        return len(' '.join(texts).split())

    @property
    def data_columns(self) -> list[str]:
        """
        Get the columns of the dataset.
        """
        columns = self.data.columns
        return columns

    @property
    def party_count(self) -> int:
        """
        The number of parties in dataset.
        """
        parties = self.data['factionId'].n_unique()
        return parties

    @property
    def available_years(self) -> list[int]:
        """
        A list of years for which data exists in the dataset.
        """
        years = self.data["year"].unique()
        return sorted(list(years))

    @staticmethod
    def get_year_from_date(date_string: str) -> str:
        """
        Extract the year from a date string.
        """
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        return str(date_object.year)

    def simple_preprocess(self, text: str) -> str:
        """
        Perform simple preprocessing on a text.
        """
        if not text:
            return ''

        # text = text.lower()
        text = re.sub(r'[,\.!?}%{}]', '', text)
        text = text.replace('\n', ' ')

        return text

    def prepare_dataset(self, data: pl.DataFrame):
        """
        Preprocess the dataset.
        """

        # preprocess text content
        data = data.with_columns(
            data["speechContent"].map_elements(
                self.simple_preprocess,
                return_dtype=str).alias("speechContent")
        )

        # add year column
        data = data.with_columns(
            data["date"].map_elements(
                self.get_year_from_date,
                return_dtype=str).alias("year")
        )

        logger.warning('finished preprocessing.')
        data.write_parquet('data/speeches_processed.parquet')
        return data

    def get_speeches_by_year(self, year) -> pl.DataFrame:
        """
        Get speeches by year.

        Args:
            year (int): The year to filter speeches by.

        Returns:
            pl.DataFrame: The filtered speeches for the given year.
        """
        year_speeches = self.data.filter(pl.col('year') == year)
        year_speeches = year_speeches.filter(pl.col('speechContent') != '')
        return year_speeches

    def get_speeches_by_party(self, party: int | str) -> list[str]:
        """
        Get speeches by party.

        Args:
            party: The party ID or abbreviation to filter speeches by.

        Returns:
            list[str]: The filtered speeches for the given party.
        """
        if isinstance(party, int):  # it is an id
            party_speeches = self.data.filter(pl.col('factionId') == party)

        if isinstance(party, str):
            id = self.factions_data.select(
                self.factions_data['abbreviation'] == party, 'id')
            party_speeches = self.data.filter(pl.col('factionId') == id)

        party_speeches = party_speeches.filter(pl.col('speechContent') != '')
        return party_speeches['speechContent'].to_list()

    def generate_topics(
            self,
            model: Literal['LDA', 'LSI', 'HDP'] = None,
            use_bigrams: bool = True,
            min_frequency: int = None,
            num_topics: int = 10,
            topn: int = 5,
            to_html: bool = True,
            verbose: bool = False,
            year: int = None,
            party: str = None
    ) -> None | TopicList:
        """
        Generate topics using the specified topic modelling algorithm.

        Args:
            model: The topic modelling algorithm to use.
            use_bigrams: Whether to apply bigram model.
            min_frequency: Minimum frequency of words to consider.
            num_topics: Number of topics to generate.
            topn: Number of top words to consider for each topic.
            to_html: Whether to save the output to an HTML file.
            verbose: Whether to display verbose output.
            year: The year to filter speeches by.
            party: The party to filter speeches by.

        Returns:
            None | TopicList: A TopicList object
            containing the generated topics,
            or None if `to_html` is True.
        """

        if year:  # filter texts by year
            year_content = self.get_speeches_by_year(str(year))
            texts = year_content['speechContent'].to_list()
            parties = year_content['factionId'].to_list()

        if party is not None:  # filter texts by party
            texts = self.get_speeches_by_party(party)

        for i, text in tqdm(enumerate(texts), total=len(texts)):
            doc = self.nlp(text)
            texts[i] = [
                tok.lemma_ for tok in doc
                if tok.pos_ in ['NOUN', 'PROPN']  # it is a noun
                   and not tok.lemma_.lower() in self.german_stop_words
                # it is not a stopword
            ]

            if verbose:
                tqdm.write(str(doc.text))

        if use_bigrams:  # apply bigram model
            bigram = gensim.models.phrases.Phrases(texts)
            texts = [bigram[line] for line in texts]

        dictionary = Dictionary(texts)

        # Filter out words that appear in less than min_frequency documents
        if min_frequency:
            dictionary.filter_extremes(no_below=min_frequency)

        corpus = [dictionary.doc2bow(text) for text in texts]

        try:
            topic_models = {
                'LDA': LdaModel(
                    corpus=corpus,
                    num_topics=num_topics,
                    id2word=dictionary
                ),
                'HDP': HdpModel(
                    corpus=corpus,
                    id2word=dictionary
                ),
                'LSI': LsiModel(
                    corpus=corpus,
                    num_topics=num_topics,
                    id2word=dictionary
                )
            }
        except ValueError:
            raise EmptyCorpusError(
                """Please modify the number of rows """
                """or the minimum frequency """
                """as the data for year {} """
                """returned an empty corpus.""".format(year)
            )

        if self.topic_model:
            model = topic_models[self.topic_model]
        else:
            model = topic_models[model]

        if to_html:
            data = pyLDAvis.gensim_models.prepare(model, corpus, dictionary)
            fname = f'src/LDA/output/topics_{str(year)}_visualized.html'
            with open(fname, 'w') as fp:
                pyLDAvis.save_html(data, fp)
                logger.warning(f'saved html file to {fname}')
        else:
            # dictionary containing the lists of salient words for each topic
            topic_words_dict = {}
            topic_distributions = []

            for topic_id in range(num_topics):
                topic_terms = model.get_topic_terms(topic_id, topn=topn)
                topic_words = [dictionary[word_id]
                               for word_id, _ in topic_terms]
                topic_words_dict[str(topic_id)] = topic_words

            # Get the topic distribution for each document
            for doc_bow in corpus:
                doc_topics = model.get_document_topics(
                    doc_bow, minimum_probability=0)
                topic_distributions.append(doc_topics)

            return TopicList(topic_words_dict, topic_distributions, parties)


def load_data(filename, n_rows=None):
    """
    Load the parquet dataset and return first n rows if specified.
    """
    assert os.path.exists(filename), "Please pass an existing file."
    data = pl.read_parquet(filename)
    if n_rows:
        data = data.limit(n_rows)
    return data


def process_topics_by_year(
        ldaModel,
        min_frequency,
        used_words,
        topic_naming_engine
):
    """
    Process topics by year using the provided LDA model and parameters.

    Args:
        ldaModel: An instance of TopicModel
        or a similar class capable of generating topics.
        min_frequency: Minimum frequency of
        words to consider during topic generation.
        used_words: A set containing words
        that have already been used as topics.
        topic_naming_engine: The engine or method used to name topics.

    Returns:
        dict: A dictionary where keys are years and values
        are dictionaries containing processed topics.
              Each topic dictionary includes:
              - 'words': A list of salient words
              associated with the topic.
              - 'relative_share': The relative share
              of the topic in the respective year.
              - 'parties': A list of parties
              associated with the topic.
    """

    topics_by_year = {}
    for year in ldaModel.available_years:
        print(f'processing year {str(year)}.')
        topics_by_year[year] = {}
        try:
            topics = ldaModel.generate_topics(
                use_bigrams=True,
                min_frequency=min_frequency,
                num_topics=5,
                topn=20,
                year=int(year),
                to_html=False)
        except EmptyCorpusError as e:
            print(EmptyCorpusError.__name__ + ": " + str(e))
            continue

        for word_list, relative_share, parties in topics:
            topic = Topic(
                salient_words=word_list,
                used_topics=used_words,
                engine=topic_naming_engine)
            topic_name = topic.name.strip(""".'"!,""")
            used_words.add(topic_name)

            print("topic: {}".format(topic_name))
            print("words: {}.".format(str(word_list)))
            print("parties: {}".format(parties))
            print("-" * 64)

            if topic_name in topics_by_year[year]:
                t = topics_by_year[year][topic_name]
                word_list = sorted(list(set(t['words'] + list(word_list))))
                relative_share = float(t['relative_share']) + relative_share
                parties = set(t['parties']).union(parties)

            topics_by_year[year][topic_name] = {
                'words': list(word_list),
                'relative_share': str(relative_share),
                'parties': list(parties)
            }
    return topics_by_year


def save_topics(output_path, topics_by_year):
    """
    Save the output dictionary to a json file.
    """
    with open(output_path, 'w', encoding='utf-8') as fp:
        json.dump(topics_by_year, fp, indent=4)


def main(args):
    """
    Run the LDA topic modelling using the
    specified arguments.
    """
    assert args.model in ['LDA', 'LSI', 'HDP'], \
        "The available models are LDA, LSI and HDP"
    assert 0 < args.min_frequency <= 1000, \
        "The minimum frequency must be between 0 and 1000"

    data = load_data(args.filename, args.n_rows)
    ldaModel = TopicModel(data, process=False, topic_model=args.model)
    used_words = set((
        "Außenpolitik",
        "Innenpolitik",
        "Regierungspolitik",
        "Gesetzesgebung",
        "Bundeswehr",
        "Klimapolitik",
        "Immigrationspolitik",
        "Wirtschaftspolitik",
        "Oppositionspolitik"
    ))
    topics_by_year = process_topics_by_year(
        ldaModel, args.min_frequency, used_words, args.topic_naming_engine)
    save_topics(args.output, topics_by_year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', default='LDA',
                        required=False, type=str)
    parser.add_argument('-minf', '--min-frequency',
                        default=20, required=False, type=int)
    parser.add_argument('-fname', '--filename',
                        default='data/speeches_processed.parquet', type=str)
    parser.add_argument('-fname1', '--filename1',
                        default='data/factions.parquet', type=str)
    parser.add_argument('-output', '--output',
                        default='topics_by_year.json', type=str)
    parser.add_argument('-n-rows', '--n-rows', default=None,
                        type=int)
    parser.add_argument('-engine', '--topic-naming-engine',
                        default='list', type=str)

    args = parser.parse_args()

    main(args)
