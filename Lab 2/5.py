def ex5(a, b):
    del a[b : len(a)]
    print(a)

ex5([int(i) for i in input().split()], int(input()))