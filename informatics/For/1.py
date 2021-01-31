def abc(n, m):
    import math
    i = math.gcd(n, m)
    return n/i, m/i
a = int(input())
b = int(input())
print(abc(a, b))
