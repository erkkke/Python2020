import math

def f(x):
    if x == 1:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

list1 = list(range(1, 1000))

list2 = [i for i in list1 if f(i)]

print(list2)