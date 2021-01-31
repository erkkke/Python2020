import re
txt = str(input())
patt = str(input())
repl = str(input())
ex = str(input())
cnt = 0

result = re.sub(patt, repl, txt)
result1 = re.findall(ex, result)
print(len(result1))