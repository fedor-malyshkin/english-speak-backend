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
    return {field: m[field].strip() for field in fields if m.get(field, None) is not None}


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

    def count(self):
        m = {}
        for entry in self.data:
            CsvToJson.put_to_map(m, entry)
        for key in m.keys():
            CsvToJson.enumerate_keys(m, key)

    @staticmethod
    def put_to_map(m, entry):
        entry_name = entry['plain_name']
        if entry_name not in m:
            m[entry_name] = [entry]
        else:
            arr = m[entry_name]
            arr.append(entry)
            m[entry_name] = arr

    @staticmethod
    def enumerate_keys(m, key):
        lst = m[key]
        length = len(lst)
        if length > 1:
            for ndx in range(1, length + 1):
                el = lst[ndx - 1]
                if 'note' in el:
                    nt = el['note']
                    nt = ', '.join([nt, 'var ' + str(ndx)])
                    nt = nt.replace(',,', ',')
                    el['note'] = nt
                else:
                    nt = 'var ' + str(ndx)
                    el['note'] = nt


if __name__ == "__main__":
    cnv = CsvToJson()
    # cnv.read("data/csv/phrasal_verbs.csv")
    cnv.read("data/csv/phrasal_verbs_raw.csv")
    cnv.count()
    cnv.output("data/phrasal_verbs.json", ["name", "meaning", "sample", "note"])
