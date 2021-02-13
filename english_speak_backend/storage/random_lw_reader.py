import csv
import random


def convert_to_map(row):
    return {'name': row[0], 'meaning': row[1], 'sample': row[2], 'note': row[3]}


class RandomLWReader:
    def __init__(self):
        self.data = []
        random.seed()

    def read(self):
        with open("data/csv/lw.csv") as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            self.data = [convert_to_map(row) for row in reader]

    def output(self):
        ndx = random.randrange(0, len(self.data))
        map = self.data[ndx]
        name, meaning, sample, note = map['name'], map['meaning'], map['sample'], map['note']
        print(f"""
==> {name}
**> {meaning} ({sample})
__> {note}
        """)


if __name__ == "__main__":
    cnv = RandomLWReader()
    cnv.read()
    cnv.output()
    cnv.output()
