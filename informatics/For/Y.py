n = int(input())
k = 0
value = 1
for i in range(n):
    print(value, end=' ')
    k += 1
    if k == value:
        k = 0
        value += 1