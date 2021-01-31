import os
s = os.getcwd()
a = os.listdir(s)
for ent in a:
    if os.path.isfile(os.path.join(s, ent)):
       print(ent)
# OR
for ent in os.scandir(s):
    if ent.is_file():
        print(ent.name)
        
#чтобы вывести все папки:
for ent in os.scandir(s):
    if ent.is_dir():
        print(ent.name)
