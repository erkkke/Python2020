import math
s = input()
n = math.ceil(len(s) / 2)
print(s[n:] + s[:n])