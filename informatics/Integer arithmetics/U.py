a = int(input())
b = int(input())
if b % a != 0:
    print(b // a + 1)
else:
    print(b // a)