s = str(input())
cnt = 0
if s.count('f') == 1:
    print(-1)
elif s.count('f') < 1:
    print(-2)    
else:
    for i in range(0, len(s)):
        if s[i] == 'f':
            cnt += 1
            if cnt == 2:
                print(i)