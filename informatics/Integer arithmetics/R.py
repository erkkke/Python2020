a = int(input())
time = (45 * a)
even = 0
odd = 0
for i in range (1, a, 2):
    if(i < a):
        odd = odd + 1
for i in range (2, a, 2):
    if(i < a):
        even = even + 1
time = time + (odd * 5) + (even * 15)
hour = (time // 60) + 9
min = time % 60
print (hour, min)

