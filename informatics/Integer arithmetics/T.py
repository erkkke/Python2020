h1 = int(input())
m1 = int(input())
s1 = int(input())
h2 = int(input())
m2 = int(input())
s2 = int(input())
h2 = h2 - h1
m2 = m2 - m1
s2 = s2 - s1
time = h2 * 60 * 60 + m2 * 60 + s2
print(time)