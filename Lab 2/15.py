def numb(a):
    b = []
    cnt = 0
    for pos in range(len(a)):
        if pos % 2 == 0:
            b.append(a[pos])
    for pos in range(len(b)):
        if b[pos] % 2 == 1:
            cnt +=1
    print(cnt)
a = int(input())
alist = [int(input()) for i in range(a)]
numb(alist)