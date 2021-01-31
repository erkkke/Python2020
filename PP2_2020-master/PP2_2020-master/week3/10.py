# d = {"Askar": 23, "BBB": 12, "CCC": 16}

# import json
# with open("out.txt", "w") as f:
#     json.dump(d, f)

# with open("out.txt", "r") as f:
#     d = json.load(f)
# print(d)

titles = ["Имя", "Фамилия", "Баллы"]
l1 = ["Askar", "Akshabayev", "3"]
l2 = ["Mansur", "Tolkabayev", "4"]

iterable = []
iterable.append(titles)
iterable.append(l1)
iterable.append(l2)

import csv
with open("1.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(iterable)