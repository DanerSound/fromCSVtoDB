import csv

raw_list = []

with open ("./friends.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        for item in row:
            raw_list.append(item.split("\t"))
    
    print(raw_list)