import argparse

import polars as pl


def main():
    parser = argparse.ArgumentParser(
        description="Convert files to .parquet format"
    )

    parser.add_argument(
        "speeches",
        type=str,
        help="The speeches.csv file"
    )

    parser.add_argument(
        "politicians",
        type=str,
        help="The politicians.tab file"
    )

    parser.add_argument(
        "factions",
        type=str,
        help="The factions.tab file"
    )

    parser.add_argument(
        "-o1",
        "--output1",
        type=str,
        default="../data/speeches.parquet",
        help="The output file path for the speech dataframe"
    )

    parser.add_argument(
        "-o2",
        "--output2",
        type=str,
        default="../data/politicians.parquet",
        help="The output file path for the politicians dataframe"
    )

    parser.add_argument(
        "-o3",
        "--output3",
        type=str,
        default="../data/factions.parquet",
        help="The output file path for the factions dataframe"
    )

    args = parser.parse_args()

    # Read the .csv file
    df_speeches = pl.read_csv(args.speeches)

    # Write to a .parquet file
    df_speeches.write_parquet(args.output1)

    print(f"Converted speeches file has been written to {args.output1}")

    # Read the .tab file
    df_politicians = pl.read_csv(args.politicians, separator="\t")

    # Write to a .parquet file
    df_politicians.write_parquet(args.output2)

    print(f"Converted politicians file has been written to {args.output2}")

    # Read the .tab file
    df_factions = pl.read_csv(args.factions, separator="\t")

    # Write to a .parquet file
    df_factions.write_parquet(args.output3)

    print(f"Converted factions file has been written to {args.output3}")


if __name__ == "__main__":
    main()
