import argparse
import json
import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def load_data(input_file: str) -> dict:
    """Load the JSON data from a file."""
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def generate_word_clouds(data: dict,
                         output_dir: str,
                         output_format: str) -> None:
    """Generate and save word clouds for each year."""
    for year, topics in data.items():
        # Combine words from all topics for the year
        all_words = []
        for topic, content in topics.items():
            all_words.extend(content['words'])

        # Create a word cloud
        wordcloud = (WordCloud(width=800, height=400,
                               background_color='white')
                     .generate(' '.join(all_words)))

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Save the word cloud to a file
        output_file = f"{output_dir}/wordcloud_{year}.{output_format}"
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Word Cloud for {year}')
        plt.savefig(output_file)
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate word clouds for each year from JSON data.')
    parser.add_argument('input_file',
                        help='Path to the input JSON file.')
    parser.add_argument('output_dir',
                        help='Directory to save the word clouds.')
    parser.add_argument('--output-format', default='svg',
                        help='The file format of the output '
                             'plots as file ending')
    args = parser.parse_args()

    data = load_data(args.input_file)
    generate_word_clouds(data, args.output_dir, args.output_format)
