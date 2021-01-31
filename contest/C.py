a = list(map(int, input().split()))
b = list(map(int, input().split()))

arsenal = a[1] + b[0]
barsa = a[0] + b[1]

if arsenal > barsa:
    print('Arselona')
    print(barsa, arsenal)
elif barsa > arsenal:
    print('Barsenal')
    print(barsa, arsenal)
elif barsa == arsenal:
    if a[1] > b[1]:
        print('Arselona')
        print(barsa, arsenal)
    elif b[1] > a[1]:
        print('Barsenal')
        print(barsa, arsenal)
    elif b[1] == a[1]:
        print('Friendship')
        print(barsa, arsenal)