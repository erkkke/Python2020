def get_sum(path):
    file = open(path)
    s = file.readline()
    l = s.split()
    return l

# "1 2 3" -> 6
def get_str_sum(s):
    list = s.split()
    sum = 0
    for l in list:
        sum += int(l)
    return sum

with open("1.txt") as file:
    for line in file:
        print(get_str_sum(line))
