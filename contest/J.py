s = str(input())

l = []
for i in range(len(s)):
    if (s[i] in l):
        l.remove(s[i])
    else:
        l.append(s[i])
if (len(s)% 2 == 0 and len(l) == 0 or (len(s) % 2 == 1 and len(l) == 1)):
    print("ZA WARUDO TOKI WO TOMARE")
else:
    print("JOJO")