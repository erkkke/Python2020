def get(path):
    file = open(path)
    s = file.readline()
    l = s.split()
    return l

list = get("1.txt")
sum = 0
for l in list:
    sum += int(l)
print(sum)


