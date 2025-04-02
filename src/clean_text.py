import argparse

import polars as pl


def clean_text(speeches: pl.DataFrame, column: str) -> pl.DataFrame:
    """
    Clean the text in a specified column of a DataFrame containing speeches.

    Args:
        speeches (pl.DataFrame): A DataFrame containing speeches or text data.
        column (str): The name of the column in `speeches` that contains
        the text to clean.

    Returns:
        pl.DataFrame: A new DataFrame with the specified column's text cleaned
        by removing
                     occurrences of '\n', '\n{..}', and '({..})'.
    """
    # Remove all occurrences of '\n', '\n{..}', and '({..})'
    text = speeches.with_columns(
        pl.col(column)
        .str.replace_all(r'\n\{.*?}', '')
        .str.replace_all(r'\(\{.*?\}\)', '')
        .str.replace_all(r'\n', ' ')
    )

    text.filter(pl.col(column).is_not_null())

    return text


def main():
    parser = argparse.ArgumentParser(
        description="A list of cleaned speech texts where certain patterns "
                    "and newline characters have been removed or replaced "
                    "with spaces."
    )

    parser.add_argument(
        "speech",
        type=str,
        help="A Dataframe of speech texts to be cleaned"
    )

    parser.add_argument(
        "column",
        type=str,
        help="The column containing the speech content"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="../data/cleaned_speech.parquet",
        help="The output file path for the cleaned speech list"
    )

    args = parser.parse_args()

    cleaned_speeches = clean_text(pl.read_parquet(args.speech),
                                  args.column)

    # Write the DataFrame to a Parquet file
    cleaned_speeches.write_parquet(args.output)

    print(f"Cleaned speeches have been written to {args.output}")


if __name__ == "__main__":
    main()
