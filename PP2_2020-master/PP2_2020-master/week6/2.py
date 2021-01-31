def z():
    print("Hello world")

def f(x):
    if callable(x):
        x()
    else:
        print(x)

f(z)
f(5)

# x = 5
# print(callable(x))

# def testFunction():
#   print("Test")

# y = testFunction
# y()
# print(callable(y))
