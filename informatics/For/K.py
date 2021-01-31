a, b = int(input()), int(input())
for i in range(a + (a % 2), b + 1, 2):
    print(i)