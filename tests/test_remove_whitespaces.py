import unittest

import polars as pl

import src.remove_whitespaces as remove_whitespaces


class TestRemoveWhitespaces(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pl.DataFrame({
            "speech_id": [1, 2, 3],
            "speech": [
                "This  is a  test speech.",
                "  Another speech with extra spaces.  ",
                "No extra spaces in this speech."
            ]
        })

    def test_remove_whitespaces(self):
        # Test if the remove_whitespaces function removes
        # extra whitespaces correctly
        cleaned_df = (remove_whitespaces
                      .remove_whitespaces(self.df, "speech"))

        expected_speeches = [
            "This is a test speech.",
            "Another speech with extra spaces.",
            "No extra spaces in this speech."
        ]

        actual_speeches = cleaned_df["speech"].to_list()

        self.assertListEqual(actual_speeches, expected_speeches)

    def test_remove_whitespaces_no_extra_spaces(self):
        # Test if the cleaned DataFrame does not contain
        # entries with leading or trailing spaces
        cleaned_df = (remove_whitespaces
                      .remove_whitespaces(self.df, "speech"))

        for speech in cleaned_df["speech"].to_list():
            self.assertFalse(speech.startswith(" "))
            self.assertFalse(speech.endswith(" "))

    def test_remove_whitespaces_structure(self):
        # Test if the cleaned DataFrame has the expected
        # structure after whitespace removal
        cleaned_df = (remove_whitespaces
                      .remove_whitespaces(self.df, "speech"))

        self.assertListEqual(cleaned_df.columns, ["speech_id", "speech"])
        self.assertEqual(cleaned_df.height, 3)


if __name__ == "__main__":
    unittest.main()
