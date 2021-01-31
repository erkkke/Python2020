try:
    print(min(int(i) for i in input().split() if int(i) % 2 != 0))
except: print(0)