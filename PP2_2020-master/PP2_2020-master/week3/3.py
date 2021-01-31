list1 = ["Almas", "Aidar", "Zhanel", "Madiyar"]
list2 = [18, 23, 34, 25]

list3 = [(list1[i], list2[i]) for i in range(0, len(list1))]

print(list3)

# list3 = zip(list1, list2)

# for i in list3:
#     print(i)