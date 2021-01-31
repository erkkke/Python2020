n = int(input())
l = list(map(int, input().split()))
unique = list(set(l))
if len(l) == len(unique):
    print("YES")
    print(unique)
else:
    print("NO")
