n = int(input())
l = list(map(int, input().split()))
b = max(l)
for i in range(len(l)):
    if l[i] == b:
        print(i)