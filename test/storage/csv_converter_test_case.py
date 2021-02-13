import unittest

from english_speak_backend.storage.csv_converter import CsvConverter
from english_speak_backend.storage.csv_converter2 import CsvConverter2


class CsvConverterTestCase(unittest.TestCase):
    def test_remove_smb_sth(self):
        result = CsvConverter.convert_original_name("ask for sb/sth")
        self.assertEqual(result, "ask for")

    def test_remove_sample(self):
        result = CsvConverter.remove_original_sample(
            "to make a light stop shining by pressing or moving a switch (Did you put the lights out downstairs?)")
        self.assertEqual(result, "to make a light stop shining by pressing or moving a switch")

    def test_extract_sample(self):
        result = CsvConverter.extract_original_sample(
            "to make a light stop shining by pressing or moving a switch (Did you put the lights out downstairs?)")
        self.assertEqual(result, "Did you put the lights out downstairs?")

    def test_first_last_middle_name(self):
        result = CsvConverter.convert_ep_name("red")
        self.assertEqual("", "")

    def test_separation(self):
        result = CsvConverter2.extract_name_and_meaning("BI: back to back = consecutive")
        self.assertEqual(("BI: back to back", "consecutive"), result )
