import argparse

import polars


def merge_tables(table1_path, table2_path, foreign_key, data_columns, id_column, output_path):
    """
    This method merges 1+ data columns from table 2 to table 1. It performs a left join.
    :param table1_path: file path to table 1
    :param table2_path: file path to table 2
    :param foreign_key: foreign key in table 1
    :param data_columns: columns of table 2 to be copied into table 1
    :param id_column: table 2 column that matches the foreign key of table 1
    :param output_path: output file path (.parquet)
    """
    # Load tables, only select the necessary rows in table 2
    df1 = polars.scan_parquet(table1_path)
    df2 = (polars.scan_parquet(table2_path)
           .select([id_column] + data_columns))
    # perform left join on table 1
    merged_table = df1.join(df2, left_on=foreign_key,
                            right_on=id_column, how='left')
    merged_table.sink_parquet(output_path)


def main():
    parser = argparse.ArgumentParser(description='Merges two parquet tables by '
                                                 'performing a left join '
                                                 'of table '
                                                 '1 with specified columns from '
                                                 'table 2')

    parser.add_argument('table1', type=str,
                        help='The feather file that should be modified')
    parser.add_argument('table2', type=str,
                        help='The feather file that contains the '
                             'additional information')
    parser.add_argument('table1_foreign_key_column_name', type=str,
                        help='The name of the column that connects entries '
                             'from table 1 with entries from table 2')  #
    parser.add_argument('data_columns', nargs='+', type=str,
                        help='The name of the column that should be copied')
    parser.add_argument('-i', '--id', default='id',
                        help='The name of the table 2 id column')
    parser.add_argument('-o', '--output', default='merged.parquet',
                        help='The name of the output file')

    args = parser.parse_args()

    merge_tables(args.table1, args.table2, args.table1_foreign_key_column_name, args.data_columns,
                 args.id, args.output)


if __name__ == '__main__':
    main()
