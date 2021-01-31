n = int(input())
for i in range(100, 1000):
    if n == (i // 100) + (i % 10) + ((i % 100) // 10):
        print(i)