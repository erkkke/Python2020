n = int(input())
n1 = n // 1000
n2 = (n // 100) % 10
n3 = n // 10 - n1 * 100 - n2 * 10
n4 = n % 10
s1 = (n1 - n4) ** 2
s2 = (n2 - n3) ** 2
print(s2 + s1 + 1)