import csv
import re

from english_speak_backend.storage import builder

REGEXP_MEANING_SAMPLE = r'\((.*)\)'
REGEXP_NOTE_VARIANT = r'var\. [0-9]'


def convert_to_map(row):
    return {'name': row[0], 'meaning': row[1], 'sample': row[2], 'note': row[3]}


class CsvConverter2:
    def __init__(self):
        self.orig = []
        self.additional = []
        self.aggregated = []

    def read(self):
        phrasal_verbs_data = builder.flat_file_pairs("data/expressions.list")
        self.orig = phrasal_verbs_data.get_all()
        with open("data/csv/lw-output.csv") as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            self.additional = [convert_to_map(row) for row in reader]

    @staticmethod
    def convert_ep(m):
        m['plain_name'] = CsvConverter2.remove_spare_spaces(m['name'])
        m['meaning'] = CsvConverter2.remove_spare_spaces(m['meaning'])
        m['sample'] = CsvConverter2.remove_spare_spaces(m['sample'])
        m['note'] = CsvConverter2.remove_spare_spaces(m['note'])
        return m

    @staticmethod
    def convert_ep_name(name):
        name = name.replace("*", "").strip()
        name = name.replace("+", "").strip()
        return name

    def convert(self):
        self.additional = [CsvConverter2.convert_ep(map) for map in self.additional]
        self.orig = [CsvConverter2.convert_original(map) for map in self.orig if map['name'].startswith("LW:")]

        self.aggregated = self.orig
        self.aggregated.extend(self.additional)

    @staticmethod
    def convert_original(m):
        m['plain_name'], m['meaning'] = CsvConverter2.extract_name_and_meaning(m['name'])
        m['plain_name'] = CsvConverter2.removeLW(m['plain_name'])
        m['sample'] = CsvConverter2.remove_spare_spaces(m.get('meaning'))
        m['note'] = CsvConverter2.remove_spare_spaces(m.get('note'))
        return m

    @staticmethod
    def extract_name_and_meaning(input2):
        m = re.search(r'(.+) += (.+)', input2)
        if m is not None:
            return m.group(1).strip(), m.group(2).strip()
        else:
            return '', ''

    @staticmethod
    def convert_original_name(name):
        name = re.sub(r'(sb|sth)/(sth|sb)?', "", name).strip()
        name = re.sub(r'(smb|sth)/(sth|smb)?', "", name).strip()
        name = re.sub(r'(somewhere|sth)/(somewhere|sth)?', "", name).strip()
        name = re.sub(r' (sb|smb|somebody|someone)', "", name).strip()
        name = re.sub(r' (something|sth)', "", name).strip()
        return name

    @staticmethod
    def removeLW(input2):
        if not input2:
            return ""
        m = re.search(r'LW:(.+)', input2)
        if m is not None:
            return m.group(1).strip()
        else:
            return ""


    @staticmethod
    def extract_original_sample(input2):
        if not input2:
            return ""
        reg_expression = REGEXP_MEANING_SAMPLE
        m = re.search(reg_expression, input2)
        if m is not None:
            return m.group(1).strip()
        else:
            return ""

    @staticmethod
    def remove_original_sample(input2):
        if not input2:
            return ""
        reg_expression = REGEXP_MEANING_SAMPLE
        m = re.search(reg_expression, input2)
        if m is not None:
            return re.sub(REGEXP_MEANING_SAMPLE, "", input2).strip()
        else:
            return input2

    @staticmethod
    def remove_original_variants(input2):
        if not input2:
            return ""
        reg_expression = REGEXP_NOTE_VARIANT
        m = re.search(reg_expression, input2)
        if m is not None:
            return re.sub(REGEXP_NOTE_VARIANT, "", input2).strip()
        else:
            return input2

    @staticmethod
    def remove_spare_spaces(input2):
        if not input2:
            return ""
        return input2.replace("  ", " ")

    def output(self):
        """
        Write data to a CSV file path
        """
        with open("data/csv/lw.csv", "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['plain_name',
                             'meaning',
                             'sample',
                             'note'])
            for line in self.aggregated:
                writer.writerow([line['plain_name'],
                                 line['meaning'],
                                 line['sample'],
                                 line['note']])


if __name__ == "__main__":
    cnv = CsvConverter2()
    cnv.read()
    cnv.convert()
    cnv.output()
