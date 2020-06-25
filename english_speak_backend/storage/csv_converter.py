from random import seed


class CsvConverter:
    def __init__(self, data):
        seed()
        self.data = data

    @staticmethod
    def convert_ep_name(value):
        return ""
