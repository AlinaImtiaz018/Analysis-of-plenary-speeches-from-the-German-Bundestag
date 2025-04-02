import unittest

import polars as pl

import src.stemming as stemming


class TestStemming(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pl.DataFrame({
            "speech_id": [1, 2, 3],
            "speech": [
                "Ich hatte einen schönen Tag.",
                "Sie gingen spazieren.",
                "Die Sonne scheint hell."
            ]
        })

    def test_stemming(self):
        # Test if stemming function correctly applies stemming
        # to the speech column
        stemmed_df = stemming.stemming(self.df, "speech")

        expected_speeches = [
            "ich hatt ein schon tag .",
            "sie ging spazi .",
            "die sonn scheint hell ."
        ]

        actual_speeches = stemmed_df["speech"].to_list()

        self.assertListEqual(actual_speeches, expected_speeches)

    def test_stemming_empty_text(self):
        # Test if the stemming function handles empty text gracefully
        empty_df = pl.DataFrame({
            "speech_id": [4],
            "speech": [""]
        })

        stemmed_empty_df = stemming.stemming(empty_df, "speech")

        self.assertEqual(stemmed_empty_df["speech"][0], "")

    def test_stemming_structure(self):
        # Test if the structure of the DataFrame remains intact after stemming
        stemmed_df = stemming.stemming(self.df, "speech")

        self.assertListEqual(stemmed_df.columns, ["speech_id", "speech"])
        self.assertEqual(stemmed_df.height, 3)


if __name__ == "__main__":
    unittest.main()
