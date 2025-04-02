import argparse
import re

import nltk
import polars as pl

nltk.download('stopwords')


def remove_stopwords(stopwords: str, speeches: pl.DataFrame, column: str) \
        -> pl.DataFrame:
    """
    Remove stopwords from a specified column in a Polars DataFrame.
    This function reads a list of stopwords from a file, compiles a
    regex pattern
    to match these stopwords, and applies this pattern to remove
    stopwords from each entry in the specified column of the given DataFrame.

    Args:
        stopwords (str): The path to a file containing stopwords, with
        one stopword per line.
        speeches (pl.DataFrame): The Polars DataFrame containing the column
        from which to remove stopwords.
        column (str): The name of the column in the DataFrame from which to
        remove stopwords.

    Returns:
        pl.DataFrame: A new DataFrame with the stopwords removed from the
        specified column.
    """
    # Read stopwords from the file
    with open(stopwords, "r") as file:
        stopwords_list = file.read().splitlines()

    stopwords_list.extend(nltk.corpus.stopwords.words('german'))

    # Create a regex pattern to match whole words in the stopwords list
    pattern = (r'(?i)\b(' + r'|'.join(re.escape(stopword) for stopword in
                                      stopwords_list) + r')\b')

    # Remove all occurrences of stopwords
    text = speeches.with_columns(
        pl.col(column)
        .str.replace_all(pattern, '')
    )

    return text


def main():
    parser = argparse.ArgumentParser(
        description="Remove stopwords from a list of speeches using a "
                    "predefined list of stopwords."
    )

    parser.add_argument(
        "stopwords",
        type=str,
        help="A list of stopwords"
    )

    parser.add_argument(
        "speech",
        type=str,
        help="A Dataframe of speech texts"
    )

    parser.add_argument(
        "column",
        type=str,
        help="The column containing the speech content"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="../data/remove_stopwords.parquet",
        help="The output file path for the removed stopword list"
    )

    args = parser.parse_args()

    removed_stopwords = remove_stopwords(args.stopwords,
                                         pl.read_parquet(args.speech),
                                         args.column)

    removed_stopwords.write_parquet(args.output)

    print(f"Removed stoppwords have been written to {args.output}")


if __name__ == "__main__":
    main()
