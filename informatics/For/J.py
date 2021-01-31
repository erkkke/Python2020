# n = int(input())
# a = '+'.join(str(i) + '*' + str(i + 1) for i in range(1, n))
# b = '='.join((a, str(eval(a))))
# print(b)

a = '+'.join(str(i) for i in range(4))
print(a)