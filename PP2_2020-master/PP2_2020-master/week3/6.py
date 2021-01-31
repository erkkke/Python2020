# 1 1 2 3 5 8
# a b
#   a b
#     a b
#       a b  
def fib():
    first = 1
    second = 1
    while True:
        yield second
        first, second = second, first + second

it_fib = fib()
print(next(it_fib))
print(next(it_fib))
print(next(it_fib))