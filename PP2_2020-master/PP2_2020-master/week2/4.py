import os
import fnmatch

with os.scandir("/Users/askar/Desktop/PP2_2020/week2") as items:
    for item in items:
        if item.is_file():
            if fnmatch.fnmatch(item.name, "*.py"):
                print(f"hello----------{item.name}")
                file = open(item.name)
                content = file.read()
                print(content)
                file.close()
