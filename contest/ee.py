import re

s = str(input())

ismail = re.search('[a-z]+@[a-z]+\.[a-z]+', s)
if ismail and ismail.span()[0] == 0 and ismail.span()[1] == len(s):
    print("Yes")
else:
    print("No")
