import os
s = os.getcwd()
a = os.scandir(s)
def d4(scandir):
    with scandir as items:
        for item in items:
            file = open(item.name)
            content = file.read()
            print(f"___________________________________{item.name}") #print("________{}".format(item.name))  
            print(content)

print(d4(a))