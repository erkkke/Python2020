list1 = [2, 6, 3, 1, 5]

# for i in list1:
#     print(i)

it = iter(list1)

while True:
    try:
        i = next(it)
        print(i)
    except StopIteration:
        break
