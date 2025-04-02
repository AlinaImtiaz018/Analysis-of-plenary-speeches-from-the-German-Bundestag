import argparse

import polars as pl


def remove_whitespaces(speeches: pl.DataFrame, column: str) -> pl.DataFrame:
    """
    Remove extra whitespaces from a specified column in a Polars DataFrame.
    This function uses Polars string manipulation methods to replace multiple
    spaces with a single space and to strip leading and trailing spaces from
    each entry in the specified column of the given DataFrame.

    Args:
        speeches (pl.DataFrame): The Polars DataFrame containing
        the column to process.
        column (str): The name of the column in the DataFrame from
        which to remove extra whitespaces.

    Returns:
        pl.DataFrame: A new DataFrame with extra whitespaces removed from
        the specified column.
    """
    text = speeches.with_columns(
        # Replace multiple spaces with a single space and strip
        # trailing spaces
        pl.col(column)
        # Replace multiple spaces with a single space
        .str.replace_all(r'  ', ' ')
        # Remove leading and trailing spaces
        .str.strip_chars()
    )

    return text


def main():
    parser = argparse.ArgumentParser(
        description="Replace double spaces with single spaces in each speech "
                    "segment of the input text and return the processed list."
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
        default="../data/remove_whitespaces.parquet",
        help="The output file path for the removed whitespace list"
    )

    args = parser.parse_args()

    remove_whitespace = remove_whitespaces(pl.read_parquet(args.speech),
                                           args.column)

    # Write the DataFrame to a Parquet file
    remove_whitespace.write_parquet(args.output)

    print(f"Removed whitespace have been written to {args.output}")


if __name__ == "__main__":
    main()
