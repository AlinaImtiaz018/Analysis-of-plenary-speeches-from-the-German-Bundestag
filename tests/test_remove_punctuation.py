import string
import unittest

import polars as pl

import src.remove_punctuation as remove_punctuation


class TestRemovePunctuation(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pl.DataFrame({
            "speech_id": [1, 2, 3],
            "speech": [
                "This? is a test sentence with punctuation.",
                "Another sentence, without punctuation!",
                "No punctuation here"
            ]
        })

    def test_remove_punctuation(self):
        # Test if remove_punctuation function correctly
        # removes punctuation from speech column
        cleaned_df = (remove_punctuation
                      .remove_punctuation(self.df, "speech"))

        expected_speeches = [
            "This is a test sentence with punctuation",
            "Another sentence without punctuation",
            "No punctuation here"
        ]

        actual_speeches = cleaned_df["speech"].to_list()

        self.assertListEqual(actual_speeches, expected_speeches)

    def test_remove_punctuation_no_punctuation(self):
        # Test if the cleaned DataFrame does not contain
        # punctuation after removal
        cleaned_df = (remove_punctuation
                      .remove_punctuation(self.df, "speech"))

        for speech in cleaned_df["speech"].to_list():
            for char in speech:
                self.assertNotIn(char, string.punctuation)

    def test_remove_punctuation_structure(self):
        # Test if the structure of the DataFrame remains
        # intact after punctuation removal
        cleaned_df = (remove_punctuation
                      .remove_punctuation(self.df, "speech"))

        self.assertListEqual(cleaned_df.columns, ["speech_id", "speech"])
        self.assertEqual(cleaned_df.height, 3)


if __name__ == "__main__":
    unittest.main()
