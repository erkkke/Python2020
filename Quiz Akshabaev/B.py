import re
a = input()
b = input()
c = re.search(b, a)
if c:
    print(f'First time {b} occured in position:', c.start())
else:
    print("Not found")