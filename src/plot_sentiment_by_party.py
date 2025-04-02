import argparse
from typing import Dict

import matplotlib.pyplot as plt
import polars as pl


def load_data(input_file: str) -> pl.DataFrame:
    """Load sentiment data from a Parquet file."""
    return pl.read_csv(input_file)


def load_factions(factions_file: str) -> Dict[int, str]:
    """Load factions data from a CSV file and return a dictionary
    mapping faction IDs to names."""
    df = pl.read_parquet(factions_file)
    return dict(zip(df['id'].to_list(), df['abbreviation'].to_list()))


def plot_sentiment_by_faction(data: pl.DataFrame,
                              factions: Dict[int, str],
                              output_file: str) -> None:
    """Plot average sentiment by faction."""
    # Associate faction IDs with names
    data = data.with_columns(pl.col('factionId')
                             .apply(lambda x: factions.get(x, 'Unknown'))
                             .alias('faction_name'))

    # Convert polars DataFrame to pandas for plotting
    df = data.to_pandas()

    # Create a bar plot
    plt.figure(figsize=(12, 8))
    plt.bar(df['faction_name'], df['avg_sentiment'], color='skyblue')
    plt.xlabel('Faction')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment by Faction')
    plt.xticks(rotation=90)
    plt.grid(True)

    # Save the plot
    plt.savefig(output_file)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot sentiment analysis by faction.')
    parser.add_argument('input_file',
                        help='Path to the input Parquet '
                             'file with sentiment data.')
    parser.add_argument('factions_file',
                        help='Path to the parquet file with faction '
                             'IDs and names')
    parser.add_argument('output_file',
                        help='Path to save the sentiment by faction plot.')
    args = parser.parse_args()

    data = load_data(args.input_file)
    factions = load_factions(args.factions_file)
    plot_sentiment_by_faction(data, factions, args.output_file)
