import json
import os
import shutil
import tempfile
import unittest

from src.plot_wordcloud_per_year import load_data, generate_word_clouds


class TestGenerateWordClouds(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

        # Create a small test JSON data
        self.test_data = {
            "1949": {
                "Regierungspolitik": {
                    "words": ["Arbeit", "Aufgabe", "Bundesregierung", "Gesetz", "Zeit"],
                    "relative_share": "0.6109600068103724",
                    "parties": [2, 4, 7, 13, 16, 20, 21, 23, 24, 25, 26, -1]
                },
                "Innenpolitik": {
                    "words": ["Volk", "Bundesregierung", "Regierung", "Land", "Recht"],
                    "relative_share": "0.16318302986324634",
                    "parties": [2, 4, 7, 13, 16, 20, 21, 23, 25, 26, -1]
                }
            }
        }

        # Write test JSON data to a file in the temporary directory
        self.input_file = os.path.join(self.test_dir, 'LDA_first1k.json')
        with open(self.input_file, 'w', encoding='utf-8') as file:
            json.dump(self.test_data, file)

        # Create a temporary directory for output
        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    def test_generate_word_clouds(self):
        # Load data
        data = load_data(self.input_file)

        # Generate word clouds
        generate_word_clouds(data, self.output_dir, "png")
        generate_word_clouds(data, self.output_dir, "svg")

        # Check if output files are created
        output_files = os.listdir(self.output_dir)
        expected_files = ['wordcloud_1949.png', 'wordcloud_1949.svg']
        self.assertTrue(all(file in output_files for file in expected_files))

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)


if __name__ == '__main__':
    unittest.main()
