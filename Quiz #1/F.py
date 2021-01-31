l1 = list(map(int, input().split()))
k = int(l1[1])
l2 = list(map(int, input().split()))
a = False
for i in range(len(l2)):
    for j in range(len(l2)):
        if (l2[i] + l2[j]) == k and i != j:
            a = True
if not a:
    print("So sad")
else:
    print("Bon Appetit")