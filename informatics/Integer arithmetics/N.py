n = int(input())
hour = n % (24 * 60) // 60
min = n % 60
print (str(hour) + " " + str(min))