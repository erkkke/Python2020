a, b = int(input()), int(input())

for i in range(a, b + 1):
    reverse = str(i)[::-1]
    if str(i) == reverse:
        print(i)


