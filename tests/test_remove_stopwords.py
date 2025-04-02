import unittest

import polars as pl

import src.remove_stopwords as remove_stopwords


class TestRemoveStopwords(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pl.DataFrame({
            "speech_id": [1, 2, 3],
            "speech": [
                "This is a test text with the stopword Kollege.",
                "Dr Paul test text Bundestag without stopwords.",
                "No stopwords here either."
            ]
        })

        # Create a sample stopwords file for testing
        stopwords_file = "data/custom_stopwords.txt"
        # with open(stopwords_file, "r") as f:
        # 	# f.write("is\nwith\na\n")
        # 	stopwords_list = f.read().splitlines()

        # self.stopwords_file = stopwords_file
        self.stopwords_file = stopwords_file

    def test_remove_stopwords(self):
        # Test if the remove_stopwords function removes stopwords correctly
        cleaned_df = (remove_stopwords
                      .remove_stopwords(self.stopwords_file, self.df,
                                        "speech"))

        expected_texts = [
            "This is a test text with the stopword .",
            " Paul test text  without stopwords.",
            "No stopwords here either."
        ]

        actual_texts = cleaned_df["speech"].to_list()

        self.assertListEqual(actual_texts, expected_texts)

    def test_remove_stopwords_no_stopwords(self):
        # Test if the cleaned DataFrame does not contain
        # stopwords after removal
        cleaned_df = (remove_stopwords
                      .remove_stopwords(self.stopwords_file, self.df,
                                        "speech"))

        for text in cleaned_df["speech"].to_list():
            for word in text.split():
                self.assertNotIn(word.lower(),
                                 ['Kollege', 'Dr', 'Bundestag'])

    def test_remove_stopwords_structure(self):
        # Test if the cleaned DataFrame has the expected structure
        # after stopwords removal
        cleaned_df = (remove_stopwords
                      .remove_stopwords(self.stopwords_file, self.df,
                                        "speech"))

        self.assertListEqual(cleaned_df.columns, ["speech_id", "speech"])
        self.assertEqual(cleaned_df.height, 3)


if __name__ == "__main__":
    unittest.main()
