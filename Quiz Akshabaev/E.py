s = input()
x = s.split()
res = len(x[0])
for i in x:
    if len(i) >= int(res):
        res = len(i)
        a = i
print(f'{a}\n{len(a)}')