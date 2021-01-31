n = int(input())
if n<86400:
    print (n//3600)
    print (n//60)
    print (n%60)
else:
    print ((n % 86400) // 3600)
    print ((n % 86400) // 60)
    print ((n % 86400) % 60)