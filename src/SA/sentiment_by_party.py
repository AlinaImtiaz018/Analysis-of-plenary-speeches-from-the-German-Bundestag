"""
Title: sentiment_by_party.py

Description:
    This file contains the method to analyze
    sentiment by political party. The function
    can be used to estimate sentiment scores
    from the speeches and factions dataset
    in parquet format.

Author:
    Alina Imtiaz,
    Universität Potsdam,
    alina.imtiaz@uni-potsdam.de

Date:
    07.07.2024

Usage:
    Pass the processed speeches_stemmed.parquet and
    factions.parquet file to analyze_sentiment_by_party
    method, and run the file using the following:
    python -m src/SA/sentiment_by_party.py --filename [filename]
"""
import argparse
import logging

import polars as pl

# from sentiment_analysis import SentimentAnalysis

logger = logging.getLogger(__name__)


def analyze_sentiment_by_party(speeches_path: str,
                               output_path: str) -> None:
    """
        Analyze sentiment of speeches by political party.

        Parameters:
        speeches_path (str): Path to the speeches Parquet file.
        factions_path (str): Path to the factions Parquet file.
        output_path (str): Path to save the output CSV file.

        Returns:
        pl.DataFrame: DataFrame containing average sentiment scores by party.
        """
    speeches = pl.read_parquet(speeches_path)
    sentiment_by_party = (speeches.group_by("factionId")
                          .agg(pl.mean("sentiment")
                               .alias("avg_sentiment")))

    sentiment_by_party.write_csv(output_path)
    logger.info(f'Saved sentiment by party to {output_path}')


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
        "-o",
        "--output",
        type=str,
        default="../data/sentiment_by_party.csv",
        help="The output file path"
    )

    args = parser.parse_args()

    analyze_sentiment_by_party(args.speeches, args.output)


if __name__ == '__main__':
    main()
