a = str(input())
x = a.split()
maxim = x[0]
for i in x:
    if len(i) > len(maxim):
        maxim = i
print(maxim, len(maxim))
