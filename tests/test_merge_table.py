import argparse
import shutil
import tempfile
import unittest
from unittest.mock import patch

import polars as pl
import polars.testing as plt

import src.merge_tables as merge_tables


class TestMergeTables(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    @patch('polars.scan_parquet')
    def test_merge_tables(self, mock_scan_parquet):
        # Create mock data for table1 and table2
        table1 = pl.LazyFrame({
            'id': [1, 2, 3],
            'foreignKey': [4, 5, 6],
            'value': ['a', 'b', 'c']
        })

        table2 = pl.LazyFrame({
            'uid': [4, 5, 6],
            'extra_info': ['x', 'y', 'z']
        })

        # Configure the mock to return the mock data
        mock_scan_parquet.side_effect = [table1, table2]

        # Expected result after merge
        expected_merged = pl.DataFrame({
            'id': [1, 2, 3],
            'foreignKey': [4, 5, 6],
            'value': ['a', 'b', 'c'],
            'extra_info': ['x', 'y', 'z']
        })

        # Call the function
        merge_tables.merge_tables('dummy_path_table1', 'dummy_path_table2',
                                  'foreignKey', ['extra_info'], 'uid',
                                  f'{self.test_dir}/dummy_out.parquet')

        result = pl.read_parquet(f'{self.test_dir}/dummy_out.parquet')

        # Check if the result is as expected
        plt.assert_frame_equal(result, expected_merged)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.merge_tables.merge_tables')
    def test_main(self, mock_merge_tables, mock_parse_args):
        # Set up the argument parser mock
        mock_parse_args.return_value = argparse.Namespace(
            table1='dummy_path_table1',
            table2='dummy_path_table2',
            table1_foreign_key_column_name='id',
            data_columns=['extra_info'],
            id='uid',
            output='dummy_out.parquet'
        )

        # Call the main function
        merge_tables.main()

        # Check if merge_tables was called with the correct arguments
        mock_merge_tables.assert_called_once_with(
            'dummy_path_table1',
            'dummy_path_table2',
            'id',
            ['extra_info'],
            'uid',
            'dummy_out.parquet'
        )

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)


if __name__ == '__main__':
    unittest.main()
