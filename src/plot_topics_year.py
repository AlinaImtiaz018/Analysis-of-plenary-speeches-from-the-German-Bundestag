import argparse
import json
from typing import Dict

import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns
from matplotlib.ticker import MaxNLocator


def load_data(json_file: str) -> Dict:
    """Load the JSON data from the specified file."""
    with open(json_file, 'r', encoding='utf-8') as fp:
        return json.load(fp)


def plot_topics(data: Dict, output_file: str, plot_type: str) -> None:
    """Plot topics over time with years on the x-axis and relative share on the y-axis."""
    plt.figure(figsize=(12, 8))  # Create a figure for the plot with specific size

    plot_data = {"year": [], "topic": [], "share": []}
    # Iterate over each year in the dataset
    for year, topics in data.items():
        # Iterate over each topic within the current year
        for topic, details in topics.items():
            plot_data["year"].append(year)
            plot_data["topic"].append(topic)
            plot_data["share"].append(float(details['relative_share']))
    df = pl.DataFrame(plot_data)

    plt.figure(figsize=(10, 6))

    if plot_type == 'scatter':
        sns.scatterplot(data=df, x='year', y='share', hue='topic')
    elif plot_type == 'line':
        sns.lineplot(data=df, x='year', y='share', hue='topic')
    else:
        raise ValueError('Argument plot_type must be "line" or "scatter"')

    plt.xlabel('Year')  # Label for the x-axis
    plt.ylabel('Relative Share')  # Label for the y-axis
    plt.title('Topics Over Time')  # Title of the plot
    plt.legend(title='Topic', loc='upper right', bbox_to_anchor=(1.3, 1))  # Place legend outside the plot

    # Customize the number of ticks on the x and y axes
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=5, prune='both'))

    plt.grid(True)  # Enable grid for better readability
    plt.tight_layout()  # Adjust the layout to fit all elements
    plt.savefig(output_file)  # Save the plot to the specified file
    plt.close()  # Close the plot to free up resources


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot topics over time.')
    parser.add_argument('json_file', help='Path to the JSON file with topics.')
    parser.add_argument('output_file', help='Path to save the plot image.')
    parser.add_argument('--plot-type', default='scatter', choices=['line', 'scatter'],
                        type=str, help="Choose the type of plot, either scatter or line plot")
    args = parser.parse_args()

    data = load_data(args.json_file)
    plot_topics(data, args.output_file, args.plot_type)
