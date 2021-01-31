def get_sum(a):
    list = a.split()
    sum = 0
    for l in list:
        sum += int(l)
    return sum

with open("2.txt") as file:
    for line in file:
        print(get_sum(line))