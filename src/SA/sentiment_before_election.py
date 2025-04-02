"""
Title: sentiment_before_election.py

Description:
    This file contains the method to analyze
    sentiment before election. The function
    can be used to estimate sentiment scores
    from the speeches and election dates dataset
    in parquet format.

Author:
    Alina Imtiaz,
    Universität Potsdam,
    alina.imtiaz@uni-potsdam.de

Date:
    07.07.2024

Usage:
    Pass the processed speeches_stemmed.parquet and
    election_dates.parquet file to analyze_sentiment_before_election
    method, and run the file using the following:
    python -m src/SA/sentiment_before_election.py --filename [filename]
"""
import argparse
import logging

import polars as pl

logger = logging.getLogger(__name__)

"""
Analyze sentiment of speeches given the year before the most 
recent election.
Parameters:
speeches_path (str): Path to the speeches Parquet file.
election_path (str): Path to the election Parquet file.
output_path (str): Path to save the output CSV file.
Returns:
pl.DataFrame: DataFrame containing dates and sentiment scores.
"""


def analyze_sentiment_before_election(speeches_path: str,
                                      election_path: str,
                                      output_path: str) -> None:
    speeches = pl.read_parquet(speeches_path)
    speeches = (speeches.with_columns(pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d")
                                      .map_elements(lambda x: x.year, return_dtype=pl.Int64).alias("year")))

    election = pl.read_csv(election_path)

    election = election.with_columns(pl.col("electionDate")
                                     .str
                                     .strptime(pl.Date, format="%d.%m.%Y"))

    sentiment_before_election = pl.DataFrame(schema={"year": pl.Int64,
                                                     "sentiment": pl.Float64})

    for row in election.iter_rows(named=True):
        election_date = row["electionDate"]
        election_year = election_date.year
        year_before_election = str(election_year - 1)

        sentiment_before_election = (sentiment_before_election
                                     .vstack(speeches.filter(speeches["year"] == year_before_election)
                                             .groupby("year")
                                             .agg(pl.mean("sentiment"))
                                             .select(["year", "sentiment"])))

    sentiment_before_election.write_csv(output_path)
    logger.info(f'Saved sentiment before election to {output_path}')


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
        "election_dates",
        type=str,
        help="Path to parquet file with table containing election_dates"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="../data/sentiment_before_election.csv",
        help="The output file path"
    )

    args = parser.parse_args()

    analyze_sentiment_before_election(args.speeches,
                                      args.election_dates,
                                      args.output)


if __name__ == '__main__':
    main()
