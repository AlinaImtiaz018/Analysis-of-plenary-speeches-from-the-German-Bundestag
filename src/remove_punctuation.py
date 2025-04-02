import argparse
import re
import string

import polars as pl


def remove_punctuation(speeches: pl.DataFrame, column: str) -> pl.DataFrame:
    """
    Remove punctuation characters from a text in a specified column
    of a Polars DataFrame.

    Args:
        speeches (pl.DataFrame): A Polars DataFrame containing text data.
        column (str): The name of the column in `speeches` DataFrame where
        punctuation should be removed.

    Returns:
        pl.DataFrame: A new Polars DataFrame with the specified `column`
        containing text with punctuation removed.
    """
    # Define a regular expression pattern to match all punctuation
    punctuation_pattern = f"[{re.escape(string.punctuation)}]"

    # Remove punctuation and strip trailing spaces
    text = speeches.with_columns(
        pl.col(column)
        .str.replace_all(punctuation_pattern, "")
        .str.strip_chars()
    )

    return text


def main():
    parser = argparse.ArgumentParser(
        description="Remove punctuation characters from "
                    "each speech in the input list."
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
        default="../data/remove_punctation.parquet",
        help="The output file path for the removed puncatation list"
    )

    args = parser.parse_args()

    remove_punctuations = remove_punctuation(pl.read_parquet(args.speech),
                                             args.column)

    # Write the DataFrame to a Parquet file
    remove_punctuations.write_parquet(args.output)

    print(f"Removed puncatations have been written to {args.output}")


if __name__ == "__main__":
    main()
