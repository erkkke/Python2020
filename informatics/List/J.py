l = list(map(int, input().split()))
p = int(input())
pos = 0
while pos < len(l) and l[pos] >= p:
    pos += 1
print(pos + 1)