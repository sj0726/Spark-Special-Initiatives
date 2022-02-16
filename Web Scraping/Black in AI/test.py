import csv
from fileinput import filelineno

occupation = ['ph', 'lecture', 'doc', 'post', 'prof']
selected = []

with open("Members.csv") as f:
    csvreader = csv.reader(f)
    fields = next(csvreader)
    for row in csvreader:
        # print(row[2])
        current = str.lower(row[2])
        if any(map(current.__contains__, occupation)):
            print(current)
            selected.append(row)
    print(selected)

file = open("Black in AI.csv", "w")
with file:
    write = csv.writer(file)
    write.writerows(selected)