a = int(input())
i = 0
while (2 ** i) <= a:
    if 2 ** i == a:
        print("YES")
        exit()
    i += 1
print("NO")