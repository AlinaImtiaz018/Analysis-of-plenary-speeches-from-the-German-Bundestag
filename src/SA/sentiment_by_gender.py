"""
Title: sentiment_by_gender.py

Description:
    This file contains the method to analyze 
    sentiment by gender. The function 
    can be used to estimate sentiment scores
    from the speeches and gender columns from 
    the dataset in parquet format.

Author:
    Alina Imtiaz,
    Universität Potsdam,
    alina.imtiaz@uni-potsdam.de

Date:
    07.07.2024

Usage:
    Pass the processed speeches_stemmed_with_gender.parquet
    and the politicians.parquet file to analyze_by_gender 
    method, and run the file using the following:
    python -m src/SA/sentiment_by_gender.py --filename [filename]
"""
import argparse
import logging

import polars as pl

from sentiment_analysis import SentimentAnalysis

logger = logging.getLogger(__name__)


def analyze_sentiment_by_gender(speeches_path: str,
                                output_path: str) -> None:
    """
        Analyze sentiment of speeches by gender of the politicians.

        Parameters:
        speeches_path (str): Path to the speeches Parquet file.
        politicians_path (str): Path to the politicians Parquet file.
        output_path (str): Path to save the output CSV file.

        Returns:
        pl.DataFrame: DataFrame containing average sentiment scores by gender.
        """
    speeches = pl.read_parquet(speeches_path)

    sentiment_analyzer = SentimentAnalysis(analyzer='nltk')

    sentiment_by_gender = (speeches.filter(speeches["gender"] != "NA")
                           .group_by("gender")
                           .agg(pl.mean("sentiment")
                                .alias("avg_sentiment")))

    sentiment_by_gender.write_csv(output_path)
    logger.info(f'Saved sentiment by gender to {output_path}')


def main():
    parser = argparse.ArgumentParser(
        description="Analyze sentiment by gender"
    )
    parser.add_argument(
        "speeches",
        type=str,
        help="Path to parquet file with table containing speeches"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="../data/sentiment_by_gender.csv",
        help="The output file path"
    )

    args = parser.parse_args()

    analyze_sentiment_by_gender(args.speeches, args.output)


if __name__ == '__main__':
    main()
