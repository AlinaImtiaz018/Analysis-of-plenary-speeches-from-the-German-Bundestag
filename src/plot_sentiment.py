import argparse

import matplotlib.pyplot as plt
import pandas as pd


def load_data(input_file: str) -> pd.DataFrame:
    """Load sentiment data from a CSV file."""
    return pd.read_parquet(input_file)


def plot_average_sentiment(data: pd.DataFrame, output_file: str) -> None:
    """Plot average sentiment over time."""
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    yearly_sentiment = data.groupby('year')['sentiment'].mean()

    plt.figure(figsize=(10, 6))
    plt.plot(yearly_sentiment.index, yearly_sentiment.values,
             marker='o', linestyle='-', color='b')
    plt.xlabel('Year')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment Over Time')
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()


def plot_sentiment_by_gender(data: pd.DataFrame, output_file: str) -> None:
    """Plot average sentiment over time by gender."""
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    yearly_sentiment_gender = (data.groupby(['year', 'gender'])['sentiment']
                               .mean()
                               .unstack())

    plt.figure(figsize=(10, 6))
    if 'weiblich' in yearly_sentiment_gender:
        plt.plot(yearly_sentiment_gender.index,
                 yearly_sentiment_gender['weiblich'],
                 marker='o', linestyle='-',
                 color='r', label='Female')
    if 'männlich' in yearly_sentiment_gender:
        plt.plot(yearly_sentiment_gender.index,
                 yearly_sentiment_gender['männlich'],
                 marker='o', linestyle='-',
                 color='b', label='Male')
    plt.xlabel('Year')
    plt.ylabel('Average Sentiment')
    plt.title('Average Sentiment Over Time by Gender')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot sentiment analysis.')
    parser.add_argument('input_file',
                        help='Path to the input CSV '
                             'file with sentiment data.')
    parser.add_argument('output_file_avg',
                        help='Path to save the average sentiment plot.')
    parser.add_argument('output_file_gender',
                        help='Path to save the sentiment by gender plot.')
    args = parser.parse_args()

    data = load_data(args.input_file)
    plot_average_sentiment(data, args.output_file_avg)
    plot_sentiment_by_gender(data, args.output_file_gender)
