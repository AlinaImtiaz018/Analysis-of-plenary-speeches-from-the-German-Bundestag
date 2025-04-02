"""
Title: test_lda_model.py

Description:
    This file contains unit tests
    for the LDA model. The model will be tested
    using Mock values.

Author:
    Konrad Brüggemann,
    Universität Potsdam,
    brueggemann4@uni-potsdam.de

Date:
    05.07.2024

Usage:
    Run all tests using\n
    python -m unittest discover -s tests
"""

import unittest
from unittest.mock import patch, MagicMock

from src.LDA.lda_model import *


class TestLDAModel(unittest.TestCase):
    """
    Unit tests for the functions in the lda_model module.

    This class contains test cases to ensure the correct functionality of
    data loading, processing, and topic generation in the lda_model module.
    """

    @patch('os.path.exists')
    @patch('polars.read_parquet')
    def test_load_data(self, mock_read_parquet, mock_exists):
        """
        Test the load_data function to ensure it correctly reads a parquet file
        and limits the number of rows.

        Args:
            mock_read_parquet (MagicMock): Mocked polars.read_parquet function.
            mock_exists (MagicMock): Mocked os.path.exists function.
        """
        mock_exists.return_value = True
        mock_data = MagicMock()
        mock_read_parquet.return_value = mock_data

        filename = 'test.parquet'
        n_rows = 10
        data = load_data(filename, n_rows)

        mock_exists.assert_called_once_with(filename)
        mock_read_parquet.assert_called_once_with(filename)
        mock_data.limit.assert_called_once_with(n_rows)

        self.assertEqual(data, mock_data.limit.return_value)

    @patch('src.LDA.lda_model.Topic')
    def test_process_topics_by_year(self, mock_topic):
        """
        Test the process_topics_by_year function.

        This test ensures that the process_topics_by_year function correctly
        processes topics for each year, uses the provided topic naming engine,
        and updates the topics_by_year dictionary accordingly.

        Args:
            mock_topic (MagicMock): Mocked Topic class.
        """
        ldaModel = MagicMock()
        ldaModel.available_years = [2020, 2021]
        ldaModel.generate_topics.return_value = [
            (['word1', 'word2'], 0.1, ['party1', 'party2'])
        ]

        min_frequency = 5
        used_words = set(["word1"])
        topic_naming_engine = "engine"

        mock_topic_instance = mock_topic.return_value
        mock_topic_instance.name = 'test_topic'

        topics_by_year = process_topics_by_year(
            ldaModel,
            min_frequency,
            used_words,
            topic_naming_engine
        )

        self.assertIn(2020, topics_by_year)
        self.assertIn('test_topic', topics_by_year[2020])

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    def test_save_topics(self, mock_json_dump, mock_open):
        """
        Test the save_topics function.

        This test verifies that the save_topics
        function correctly writes the
        topics_by_year dictionary to a JSON file
        with the specified output path.

        Args:
            mock_json_dump (MagicMock): Mocked json.dump function.
            mock_open (MagicMock): Mocked builtins.open function.
        """
        output_path = 'output.json'
        topics_by_year = {
            '2020': {'test_topic': {
                'words': ['word1'],
                'relative_share': '0.1',
                'parties': ['party1']
            }}}

        save_topics(output_path, topics_by_year)

        mock_open.assert_called_once_with(output_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once_with(
            topics_by_year, unittest.mock.ANY, indent=4)

    @patch('src.LDA.lda_model.load_data')
    @patch('src.LDA.lda_model.TopicModel')
    @patch('src.LDA.lda_model.save_topics')
    def test_main(self, mock_save_topics, mock_TopicModel, mock_load_data):
        """
        Test the main function.

        This test verifies that the main function
        correctly processes command line
        arguments, loads data, initializes the topic model,
        and saves the processed topics.

        Args:
            mock_save_topics (MagicMock): Mocked save_topics function.
            mock_TopicModel (MagicMock): Mocked TopicModel class.
            mock_load_data (MagicMock): Mocked load_data function.
        """
        args = MagicMock()
        args.model = 'LDA'
        args.min_frequency = 5
        args.filename = 'test.parquet'
        args.n_rows = None
        args.output = 'output.json'
        args.topic_naming_engine = 'engine'

        mock_load_data.return_value = MagicMock()
        mock_TopicModel.return_value = MagicMock()

        main(args)

        mock_load_data.assert_called_once_with(
            args.filename, args.n_rows)
        mock_TopicModel.assert_called_once_with(
            mock_load_data.return_value, process=False, topic_model=args.model)
        mock_save_topics.assert_called_once()


if __name__ == '__main__':
    unittest.main()
