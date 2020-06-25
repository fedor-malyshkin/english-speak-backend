import csv
import re

from english_speak_backend.storage import builder

REGEXP_MEANING_SAMPLE = r'\((.*)\)'
REGEXP_NOTE_VARIANT = r'var\. [0-9]'


def convert_to_map(row):
    return {'name': row[0], 'meaning': row[1], 'sample': row[2]}


class CsvConverter:
    def __init__(self):
        self.orig = []
        self.additional = []
        self.aggregated = []

    def read(self):
        phrasal_verbs_data = builder.flat_file_pairs("data/phrasal_verbs.list", builder.phrasal_verb_record_transformer)
        self.orig = phrasal_verbs_data.get_all()
        with open("data/csv/pv.csv") as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            self.additional = [convert_to_map(row) for row in reader]

    @staticmethod
    def convert_ep(m):
        m['plain_name'] = CsvConverter.remove_spare_spaces(CsvConverter.convert_ep_name(m['name']))
        m['note'] = ""
        return m

    @staticmethod
    def convert_ep_name(name):
        name = name.replace("*", "").strip()
        name = name.replace("+", "").strip()
        return name

    def convert(self):
        self.additional = [CsvConverter.convert_ep(map) for map in self.additional]
        self.orig = [CsvConverter.convert_original(map) for map in self.orig]

        self.aggregated = self.orig
        self.aggregated.extend(self.additional)

    @staticmethod
    def convert_original(m):
        m['plain_name'] = CsvConverter.remove_spare_spaces(CsvConverter.convert_original_name(m['name']))
        m['sample'] = CsvConverter.remove_spare_spaces(CsvConverter.extract_original_sample(m['meaning']))
        m['meaning'] = CsvConverter.remove_spare_spaces(CsvConverter.remove_original_sample(m['meaning']))
        m['note'] = CsvConverter.remove_spare_spaces(CsvConverter.remove_original_variants(m['note']))
        return m

    @staticmethod
    def convert_original_name(name):
        name = re.sub(r'(sb|sth)/(sth|sb)?', "", name).strip()
        name = re.sub(r'(smb|sth)/(sth|smb)?', "", name).strip()
        name = re.sub(r'(somewhere|sth)/(somewhere|sth)?', "", name).strip()
        name = re.sub(r' (sb|smb|somebody|someone)', "", name).strip()
        name = re.sub(r' (something|sth)', "", name).strip()
        return name

    @staticmethod
    def extract_original_sample(meaning):
        reg_expression = REGEXP_MEANING_SAMPLE
        m = re.search(reg_expression, meaning)
        if m is not None:
            return m.group(1).strip()
        else:
            return ""

    @staticmethod
    def remove_original_sample(meaning):
        reg_expression = REGEXP_MEANING_SAMPLE
        m = re.search(reg_expression, meaning)
        if m is not None:
            return re.sub(REGEXP_MEANING_SAMPLE, "", meaning).strip()
        else:
            return meaning

    @staticmethod
    def remove_original_variants(note):
        reg_expression = REGEXP_NOTE_VARIANT
        m = re.search(reg_expression, note)
        if m is not None:
            return re.sub(REGEXP_NOTE_VARIANT, "", note).strip()
        else:
            return note

    @staticmethod
    def remove_spare_spaces(word):
        return word.replace("  ", " ")

    def output(self):
        """
        Write data to a CSV file path
        """
        with open("data/csv/phrasal_verbs.csv", "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['plain_name',
                             'name',
                             'meaning',
                             'sample',
                             'note'])
            for line in self.aggregated:
                writer.writerow([line['plain_name'],
                                 line['name'],
                                 line['meaning'],
                                 line['sample'],
                                 line['note']])

    def calculate(self):
        m = {}
        m_counts = {}
        for line in self.aggregated:
            key = line['plain_name']
            lst = m.get(key, [])
            lst.append(line)
            m[key] = lst
            m_counts[key] = len(lst)


if __name__ == "__main__":
    cnv = CsvConverter()
    cnv.read()
    cnv.convert()
    cnv.calculate()
    cnv.output()
