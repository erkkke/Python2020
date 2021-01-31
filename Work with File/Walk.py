import os
s = os.getcwd()
for dir, dirs, files in os.walk(s): #все файлы папки
#os.walk(s, topdawn = True): True по умолчанию, если будет False, то он будет пробегаться в обратном порядке
    print(f"Found Directory {dir}")
    print(dirs)
    print(files)