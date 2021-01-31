l = [int(i) for i in input().split()]
index = 0
for i in range(len(l)):
    if l[i] > l[index]:
        index = i
print(l[index], index)


