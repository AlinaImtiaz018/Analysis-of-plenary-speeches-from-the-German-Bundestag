import argparse

import matplotlib.pyplot as plt
import polars as pl


def load_data(input_file: str) -> pl.DataFrame:
    """Load sentiment data from a Parquet file."""
    return pl.read_csv(input_file)


def plot_sentiment_by_gender(data: pl.DataFrame, output_file: str) -> None:
    """Plot sentiment by gender."""
    # Convert polars DataFrame to pandas for plotting
    df = data.to_pandas()

    # Create a bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(df['gender'], df['avg_sentiment'], color=['blue', 'orange'])
    plt.xlabel('Gender')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment by Gender')
    plt.grid(True)

    # Save the plot
    plt.savefig(output_file)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot sentiment analysis by gender.')
    parser.add_argument('input_file',
                        help='Path to the input Parquet file '
                             'with sentiment data.')
    parser.add_argument('output_file',
                        help='Path to save the sentiment by gender plot.')
    args = parser.parse_args()

    data = load_data(args.input_file)
    plot_sentiment_by_gender(data, args.output_file)
