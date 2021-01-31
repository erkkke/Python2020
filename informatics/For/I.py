n = int(input())
cnt = 1
l = ["+___ ", f"|{cnt} / ", r"|__\ ", "|    "]
for part in l:
    for i in range(n):
        print(str(part))
        cnt += 1
