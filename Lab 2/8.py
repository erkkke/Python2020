def minmax(a):
    b = []
    mini = 1e9
    maxi = -1e9
    for i in range(len(a)):
        if(a[i] >= maxi):
            maxi = a[i]
        if(a[i] <= mini):
            mini = a[i]
    b.append(mini)
    b.append(maxi)
    print(b)
a = int(input())
alist = [int(input()) for i in range(a)] 
minmax(alist)