# def sum(a=5, b=10):
#     """
#     doc string
#     """
#     return a + b, a - b, a * b

# a = int(input())
# b = int(input())
# c, _, _ = sum(a, b)
# print(c)

# pow2 = []
# for i in range(10):
#     pow2.append(2 ** i)

# pow2 = [2 ** x for x in range(10)]

n = int(input())
all_even = [x for x in range(n) if x % 2 == 0]
print(all_even)