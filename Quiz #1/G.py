k = int(input())
t = list(map(str, input().split()))
n = int(input())
print(int(''.join(t)[0:n]) * int(''.join(t)[n:]))