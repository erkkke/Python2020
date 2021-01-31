l = list(map(int, input().split()))
a, b = l[0], l[1]
i = 0
while a <= b:
    a *= 3
    b *= 2
    i +=1
print(i)
