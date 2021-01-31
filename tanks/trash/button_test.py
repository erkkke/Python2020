def a():
    global b
    b = 8

b = 10
a()
print(b)