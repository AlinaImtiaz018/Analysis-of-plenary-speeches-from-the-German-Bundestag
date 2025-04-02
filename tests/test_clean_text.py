import unittest

import polars as pl

import src.clean_text as clean_text


class TestCleanText(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pl.DataFrame({
            "speech_id": [1, 2, 3],
            "speech": [
                "This is a\ntest.\n{abc}\n",
                "Another\ntest. ({xyz})",
                "No newlines here."
            ]
        })

    def test_clean_text_patterns(self):
        # Test if the cleaning function removes specific patterns correctly
        cleaned_df = clean_text.clean_text(self.df, "speech")

        expected_texts = [
            "This is a test. ",
            "Another test. ",
            "No newlines here."
        ]

        actual_texts = cleaned_df["speech"].to_list()

        self.assertListEqual(actual_texts, expected_texts)

    def test_clean_text_null_values(self):
        # Test if the cleaned DataFrame does not contain null
        # values in the cleaned column
        cleaned_df = clean_text.clean_text(self.df, "speech")

        self.assertFalse(cleaned_df["speech"].null_count() > 0)

    def test_clean_text_structure(self):
        # Test if the cleaned DataFrame has the expected
        # structure after cleaning
        cleaned_df = clean_text.clean_text(self.df, "speech")

        self.assertListEqual(cleaned_df.columns, ["speech_id", "speech"])
        self.assertEqual(cleaned_df.height, 3)


if __name__ == "__main__":
    unittest.main()
