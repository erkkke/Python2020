import os
import fnmatch
s = os.getcwd()
with os.scandir(s) as entries:
    for entry in entries:
        if fnmatch.fnmatch(entry.name, "*.py"):
            print(entry.name)