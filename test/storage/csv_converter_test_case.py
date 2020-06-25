import unittest

from english_speak_backend.storage.csv_converter import CsvConverter


class CsvConverterTestCase(unittest.TestCase):
    def test_first_last_name(self):
        result = CsvConverter.convert_ep_name("seeger")
        self.assertEqual(result, "")

    def test_first_last_middle_name(self):
        result = CsvConverter.convert_ep_name("red")
        self.assertEqual("", "")
