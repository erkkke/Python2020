# for i in range(1, 10, 2): # start, end, step
#     print(i)


# list = [10, 20, 11, 34, 55]
# for i in list:
#     print(i)

# for i in range(ord('a'), ord('z') + 1):
#     print(chr(i))
from itertools import chain
import math

for i in chain(range(2, 5), range(10, 14), range(20, 25)):
    print(i)