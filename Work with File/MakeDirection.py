import os
s = os.getcwd()
os.mkdir("Hello") #для создания одной папки
os.makedirs("Hello/world/abs") #для создания нескольких
with os.scandir(s) as entries:
    if fnmatch.fnmatch(entry.name, "*.txt")