def isSet(a):
    b = set()
    for i in range(len(a)):
        b.add(a[i] - 1)
        b.add(a[i] + 1)
    b = set(b)
    print(b)
a = int(input())
alist = [int(input()) for i in range(a)] 
isSet(alist)