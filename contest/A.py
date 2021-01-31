n, m, k = int(input()), int(input()), int(input())
if k < n * m:
    if k % n == 0 or k % m == 0:
        print('YES')
        quit()
print('NO')