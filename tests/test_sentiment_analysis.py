"""
Title: test_sentiment_analysis.py

Description:
    This file contains unit tests
    for the SA module. The module will 
    be tested using Mock values.

Author:
    Alina Imtiaz,
    Universität Potsdam,
    alina.imtiaz@uni-potsdam.de

Date:
    07.07.2024

Usage:
    Run all tests using
    python -m unittest discover -s tests
"""
import unittest
from unittest.mock import patch, MagicMock

from src.SA.sentiment_analysis import SentimentAnalysis


class TestSentimentAnalysis(unittest.TestCase):
    """
    Unit tests for the functions in the sentiment_analysis module.

    This class contains test cases to ensure the correct functionality of
    sentiment analysis using different analyzers.
    """

    @patch('nltk.sentiment.vader.SentimentIntensityAnalyzer')
    def test_nltk_analyzer(self, mock_analyzer):
        """
        Test the compute_sentiment function with the NLTK analyzer.

        This test verifies that the compute_sentiment function correctly
        uses the NLTK analyzer to compute the sentiment score.

        Args:
            mock_analyzer (MagicMock): Mocked SentimentIntensityAnalyzer class.
        """
        mock_instance = mock_analyzer.return_value
        mock_instance.polarity_scores.return_value = {'compound': 0.5}

        sentiment_analysis = SentimentAnalysis(analyzer='nltk')
        sentiment_analysis.analyzer = mock_instance
        score = sentiment_analysis.compute_sentiment("This is a test.")

        self.assertEqual(score, 0.5)
        mock_instance.polarity_scores.assert_called_once_with("This is a test.")

    @patch('src.SA.sentiment_analysis.pipeline')
    def test_pytorch_analyzer(self, mock_pipeline):
        """
        Test the compute_sentiment function with the PyTorch analyzer.

        This test verifies that the compute_sentiment function correctly
        uses the PyTorch analyzer to compute the sentiment score.

        Args:
            mock_pipeline (MagicMock): Mocked pipeline function.
        """
        mock_instance = mock_pipeline.return_value
        mock_instance.return_value = [{'label': 'POSITIVE', 'score': 0.9}]

        sentiment_analysis = SentimentAnalysis(analyzer='pytorch')
        score = sentiment_analysis.compute_sentiment("This is a test.")

        self.assertEqual(score, 0.9)
        mock_instance.assert_called_once_with("This is a test.")


if __name__ == '__main__':
    unittest.main()
