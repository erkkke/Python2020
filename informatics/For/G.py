def f(a):
    b = 1
    for i in range(1, a + 1):
        b *= i
    return b
n = int(input())
k = int(input())
t = n - k
print(int(f(n) / (f(k) * f(n-k))))