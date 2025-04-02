"""
Title: topic_naming.py

Description:
    This file contains the Topic class,
    which is used to determine which topic
    a number of keywords provided by the LDA model
    belongs to.

Author:
    Konrad Brüggemann,
    Universität Potsdam,
    brueggemann4@uni-potsdam.de

Date:
    05.07.2024

Usage:
    Pass a list of extracted keywords to the class.
    Then the name property will contain the topic name,
    that was classified using SpaCy vectors.
"""

import json
from typing import Optional, Literal

import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity

from src.LDA.exceptions import *


class Topic:

    def __init__(
            self,
            salient_words: list[str],
            used_topics: list[str] = None,
            engine: Literal["list"] = "list",
    ) -> None:
        self.salient_words = salient_words
        self.engine = engine
        self.used_topics = used_topics
        self.nlp = spacy.load('de_core_news_lg')

    @property
    def name(self) -> Optional[str]:
        return self.topic_classifier_list_based()

    @staticmethod
    def average_vector(lemmata, nlp_model):
        vectors = []
        for lemma in lemmata:
            token = nlp_model.vocab[lemma]
            if token.has_vector:
                vectors.append(token.vector)
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return None

    def topic_classifier_list_based(self) -> Optional[str]:
        with open('src/LDA/topic_keywords.json', 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        topics = data['topics']
        extracted_vector = self.average_vector(self.salient_words, self.nlp)

        if extracted_vector is not None:
            # Compute cosine similarity
            # between extracted vector and topic vectors
            topic_similarities = {}
            for topic, lemma_list in topics.items():
                topic_vector = self.average_vector(lemma_list, self.nlp)
                if topic_vector is not None:
                    similarity = cosine_similarity(
                        [extracted_vector], [topic_vector]
                    )[0][0]
                    topic_similarities[topic] = similarity

            # Determine the topic with the highest similarity
            if topic_similarities:
                max_similarity_topic = max(
                    topic_similarities,
                    key=topic_similarities.get
                )
                return max_similarity_topic
            else:
                NoTopicsFoundError
        else:
            raise MissingVectorError
