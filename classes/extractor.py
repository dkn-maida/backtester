import csv
from classes.bar import Bar

class Extractor:

    def __init__(self):
        pass

    def read(self, filename):
        fields = []
        rows = []
        bars= []

        with open(filename, 'r') as e:
            csvreader = csv.reader(e)
            fields = next(csvreader)
            #print('Field names are:' + ', '.join(field for field in fields))
            for row in csvreader:
                rows.append(row)
                #print(row)
        for col in rows:
            b = Bar(col[0], float(col[1]), float(col[2]), float(col[3]), float(col[4]))
            bars.append(b)
        return bars