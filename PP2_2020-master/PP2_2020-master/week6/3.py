def f(*args):
    for i in args:
        print(i)

def f1(**kwargs):
    print(kwargs)
    # for i in kwargs:
    #     print(i)
    #     print(kwargs[i])

a = 4
b = 1
c = 2
# f(a, b, c, a, b, c)
f1(name="ABC", surname="DEF")