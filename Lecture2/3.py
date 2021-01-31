list1 = ["Almas", "Aidar", "Zhanel", "madiyar"]
list2 = [18, 23, 34,25]

list3 = zip(list1, list2)

list3 = [(list1[i], list2[i]) for i in range(0, len(list1))]
#dict = {"Almas": 18, "Aidar": 23, "Zhanel": 23, "madiyar": 25}
print(list3)