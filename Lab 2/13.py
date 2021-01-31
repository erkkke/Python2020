def isPol(a):
    leng = len(a)
    for i in range(leng // 2):
        if a[i] != a[-1 - i]:
            return "NO"
        return "YES"

b = int(input())
alist = [int(input()) for i in range(b)]
print(isPol(alist))