s = input()

# 1st way
cnt = 0
for i in range(len(s)):
    if s[i] == 'f':
        cnt += 1
        if cnt == 2:
            print(i)
            exit()
if cnt == 1:
    print(-1)
else: print(-2)

# 2nd way
if s.count('f') == 1:
    print(-1)
elif s.count('f') == 0:
    print(-2)
else:
    print(s.find('f', s.find('f') + 1))