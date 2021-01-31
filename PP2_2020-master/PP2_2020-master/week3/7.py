# Prime numbers
# 2 3 5 7 ...
import math

def is_prime(x):
    if x == 1:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

# n = 5
def next_prime():
    n = 2
    while True:
        while not is_prime(n):
            n = n + 1
        yield n
        n = n + 1

prime = next_prime()

for i in range(0, 10):
    print(next(prime))
