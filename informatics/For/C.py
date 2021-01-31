n = int(input())
lst = []
for i in range(10 ** n - 1, 0, -1):
    if i % 2 != 0:
        lst.append(i)
for i in lst:
    print(i)