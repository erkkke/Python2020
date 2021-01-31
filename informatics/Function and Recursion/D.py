def a(x, y):
    return abs(x) + abs(y) <= 1

x = float(input())
y = float(input())
if a(x, y):
    print("YES")
else:
    print("NO") 