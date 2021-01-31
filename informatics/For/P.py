a, b, c, d, e = int(input()), int(input()), int(input()), int(input()), int(input())
cnt = 0
for x in range(1001):
    if x != e:
        if (a * x**3 + b * x**2 + c * x + d) / (x - e) == 0:
            cnt += 1
print(cnt)