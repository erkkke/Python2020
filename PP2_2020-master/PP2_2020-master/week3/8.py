import math

def is_prime(x):
    if x == 1:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

list1 = list(range(1, 100))
# print(list1)

it = (x for x in list1 if is_prime(x))

print(next(it))