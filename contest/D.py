def recursion(l, r):
    if l % 2 == 0:
        recursion(l + 1, r)
        return
    if l <= r:
        print(l, end=' ')
        recursion(l + 1, r)

a = [int(i) for i in input().split()]
l, r = a[0], a[1]

recursion(l, r)