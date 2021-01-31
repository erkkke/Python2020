import os
s = os.getcwd()
a = os.scandir()
for directory, dirs, files in os.walk(s):
    for dir in dirs:
        print(dir)
        print()

    for file in files:
        ent = open(file)
        content = ent.read()
        print(f"{file}_______________________")
        print(content)
        ent.close()
        print()