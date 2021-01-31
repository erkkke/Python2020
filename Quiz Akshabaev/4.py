x = 0
y = 0

l = str(input())
x1 = int(input())
y1 = int(input())
ans = False
for i in range(len(l)):
    if (l[i] == 'R'):
        x = x + 1
    elif (l[i] == 'L'):
        x = x - 1
    elif (l[i] == 'U'):
        y = y + 1
    elif (l[i] == 'D'):
        y = y - 1
    if(x == x1 and y == y1):
        ans == True
        break
    
if(x >= x1 and y >= y1):
    print('Passed')
else:
    print('Missed')