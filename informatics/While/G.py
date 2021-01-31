x = int(input())
p = int(input())
y = int(input())
cnt = 0
while x < y:
    x *= (1 + p / 100)
    x = int(100 * x) / 100
    cnt += 1
print(cnt)