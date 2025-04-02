"""
Title: sentiment_analysis.py

Description:
    This file contains the class Sentiment Analysis.
    The Sentiment Analysis class can be used
    to estimate sentiment scores to the dataset
    in parquet format.

Author:
    Alina Imtiaz,
    Universität Potsdam,
    alina.imtiaz@uni-potsdam.de

Date:
    07.07.2024

Usage:
    Pass the processed speeches_stemmed.parquet file to the
    Sentiment Analysis class, and run the file using\n
    python -m src/SA/sentiment_analysis.py --filename [filename]
"""

import argparse
import logging

import nltk
import polars as pl
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from transformers import pipeline

nltk.download('vader_lexicon')

logger = logging.getLogger(__name__)


class SentimentAnalysis:
    """
    Class for performing sentiment analysis using different analyzers.

    Attributes:
    analyzer_type (str): Type of sentiment analyzer
    ('nltk', 'gervader', 'pytorch').
    analyzer: The sentiment analyzer object.
    """

    def __init__(self, analyzer: str = 'nltk') -> None:

        """
        Initialize the SentimentAnalysis class with the specified analyzer.

        Parameters:
        analyzer (str): The type of analyzer to use
        ('nltk', 'gervader', 'pytorch').

        Raises:
        ValueError: If an unsupported analyzer type is provided.
        """

        self.analyzer_type = analyzer
        if analyzer == 'nltk':
            self.analyzer = SentimentIntensityAnalyzer()
        elif analyzer == 'pytorch':
            self.analyzer = (pipeline('sentiment-analysis',
                                      model='nlptown/bert-base-multilingual-'
                                            'uncased-sentiment'))
        else:
            raise ValueError("Unsupported analyzer type. "
                             "Choose from 'nltk', 'gervader', or 'pytorch'.")

    def compute_sentiment(self, text: str) -> float:
        """
        Compute the sentiment score for the given text.

        Parameters:
        text (str): The text to analyze for sentiment.

        Returns:
        float: Sentiment score in the range -1 to 1.
        """
        if self.analyzer_type == 'nltk':
            score = self.analyzer.polarity_scores(text)
            return score['compound']
        elif self.analyzer_type == 'gervader':
            return self.analyzer.predict(text)['compound']
        elif self.analyzer_type == 'pytorch':
            result = self.analyzer(text)[0]
            if 'negative' in result['label'].lower():
                return -1 * result['score']
            elif 'positive' in result['label'].lower():
                return result['score']
            else:
                return 0.0


def main():
    parser = argparse.ArgumentParser(
        description="Analyze sentiment before election"
    )
    parser.add_argument(
        "speeches",
        type=str,
        help="Path to parquet file with table containing speeches"
    )

    parser.add_argument(
        "-a",
        "--analyzer",
        choices=['nltk', 'gervader', 'pytorch'],
        default='nltk',
        type=str,
        help="The sentiment analyzer to be used"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="../data/sentiment_before_election.parquet",
        help="The output file path"
    )

    args = parser.parse_args()

    speeches = pl.read_parquet(args.speeches)

    sentiment_analyzer = SentimentAnalysis(analyzer=args.analyzer)

    speeches = speeches.with_columns(
        pl.col("speechContent").map_elements(
            sentiment_analyzer.compute_sentiment,
            return_dtype=pl.Float64).alias("sentiment")
    )

    speeches.write_parquet(args.output)


if __name__ == '__main__':
    main()
