import csv

with open('api_yamdb/static/data/users.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)