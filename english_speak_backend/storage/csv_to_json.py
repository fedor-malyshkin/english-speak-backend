import csv
import json

from english_speak_backend.storage.builder import is_empty


def convert_to_map(row, fields):
    res = {}
    for ndx in range(0, len(fields)):
        if not is_empty(row[ndx]):
            res[fields[ndx]] = row[ndx]
    return res


def filter_fields(m, fields):
    return {field: m[field] for field in fields if m.get(field, None) is not None}


class CsvToJson:
    def __init__(self):
        self.fields = []
        self.data = []

    def read(self, file_name):
        with open(file_name) as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            self.fields = next(reader)
            self.data = [convert_to_map(row, self.fields) for row in reader]

    def output(self, file_name, fields):
        """
        Write data to a CSV file path
        """
        res = [filter_fields(entry, fields) for entry in self.data]

        with open(file_name, "w") as fo:
            json.dump(res, fo)


if __name__ == "__main__":
    cnv = CsvToJson()
    cnv.read("data/csv/phrasal_verbs.csv")
    cnv.output("data/phrasal_verbs.json", ["name", "meaning", "sample", "note"])
