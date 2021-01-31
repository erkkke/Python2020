import os
import fnmatch
s = os.getcwd()
with os.scandir(s) as items:
    for item in items:
        if item.is_file():
            if fnmatch.fnmatch(item.name, "*.txt"):
                file = open(item.name)
                content = file.read()
                print(f"___________________________________{item.name}") #print("________{}".format(item.name))  
                print(content)
                file.close()