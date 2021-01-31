n = int(input())
if n < 86400:
    hour = n // 3600
    min = (n % 3600) // 60
    sec = n % 60
else:
    n = n % 86400
    hour = n // 3600
    min = (n % 3600) // 60
    sec = n % 60
if min < 10:
    min = "0" + str(min)
if sec < 10:
    sec = "0" + str(sec)
print (str(hour) + ":" + str(min) + ":" + str(sec))

