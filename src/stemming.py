import argparse

import nltk
import polars as pl

# Download NLTK's punkt tokenizer if not already downloaded
nltk.download('punkt')


def stemming(speeches: pl.DataFrame, column: str) -> pl.DataFrame:
    """
    Perform stemming on a text in a specified column of a Polars DataFrame
    using NLTK's SnowballStemmer for German.

    Args:
        speeches (pl.DataFrame): A Polars DataFrame containing text data.
        column (str): The name of the column in `speeches` DataFrame where
        a text should be stemmed.

    Returns:
        pl.DataFrame: A new Polars DataFrame with the specified `column`
        containing the stemmed text.
    """
    # Initialize Snowball Stemmer for German
    snowball = nltk.stem.SnowballStemmer(language="german")

    # Apply stemming to the specified column
    text = speeches.with_columns(
        pl.col(column)
        .apply(lambda speech: " "
               .join(snowball.stem(word) for word in
                     nltk.word_tokenize(speech)),
               return_dtype=pl.String)
    )

    return text


def main():
    parser = argparse.ArgumentParser(
        description="Perform stemming on a list of German speeches "
                    "using the Snowball Stemmer."
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
        default="../data/stemming.parquet",
        help="The output file path for the stemming list"
    )

    args = parser.parse_args()

    stemm = stemming(pl.read_parquet(args.speech), args.column)

    # Write the DataFrame to a Parquet file
    stemm.write_parquet(args.output)

    print(f"Stemming have been written to {args.output}")


if __name__ == "__main__":
    main()
