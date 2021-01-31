import os


def Menu_Dir():
    print("""[1] rename directory
[2] see number of files in Directory
[3] see number of folders in Directory
[4] see list content of the directories
[5] add file to this Directory
[6] add new folder to this Directory
[7] work with files
[0] exit""")


def Menu_File():
    print("""[1] delete file
[2] rename file
[3] add content to file
[4] rewrite content of file
[5] content of files
[6] work with directories
[0] exit""")


# Cleaning of TERMINAL
def clear():
    enter = input("Tap [ENTER] to continue\n")
    if enter == "":
        os.system("cls")


# WORK WITH DIRECTORY ________________________________________________________________________

# Rename directory
def d1(s):
    prev_name = os.path.join(s, input("Enter directory name: "))
    new_name = os.path.join(s, input("Enter new directory name: "))
    if os.path.exists(prev_name):
        os.rename(prev_name, new_name)
        print("Directory renamed\n")
    else:
        print("Error, directory does not exist\n")
    clear()


# See number of files in it
def d2(scandir):
    cnt = 0
    for item in scandir:
        if item.is_file():
            cnt += 1
    print(f"{cnt} file(s) in directory")
    clear()


# See number of directories in it
def d3(scandir):
    cnt = 0
    for item in scandir:
        if item.is_dir():
            cnt += 1
    print(f"{cnt} folder(s) in directory")
    clear()


# See list content of the directory
def d4(scandir):
    for item in scandir:
        if item.is_dir():
            print(item.name)
    clear()


# Add new file to this directory
def d5(s):
    name = input("Enter new file's name: ")
    file = open(os.path.join(s, name), mode = "w")
    print(f"File {name} created\n")
    file.close()
    clear()


# Add new folder to this directory
def d6(s):
    name = input("Enter the new directory's name: ")
    folder = os.mkdir(s + "//" + name)
    print(f"Directory {name} created\n")
    clear()


# WORK WITH FILES ___________________________________________________________________________


# Delete file
def f1(s):
    name = input("Name of the file which you want to remove: ")
    path = s + "/" + name
    if os.path.exists(path) and os.scandir(path).is_file():
        os.remove(path)
        print(f"File {name} is removed\n")
    else:
        print(f"File {name} does not exist\n")
    clear()


# Rename file
def f2(s):
    prev_name = os.path.join(s, input("Enter file's name: "))
    if os.path.exists(prev_name):
        new_name = os.path.join(s, input("Enter file's new name: "))
        os.rename(prev_name, new_name)
        print("File renamed\n")
    else:
        print("Error, file does not exist\n")
    clear()


# Add content to file
def f3(s):
    path_to_file = os.path.join(s, input("Name of the file which you want to add content: "))
    if os.path.exists(path_to_file):
        with open(path_to_file, mode = 'a') as file:

            print("You can write content here!")
            print("If you want to finish, just press [ENTER] in empty line")

            content = input("\n")
            while content != "":
                file.write(f"{content}\n")
                content = input()
            print("File succefully edited\n")

    else:
        print("Error, file does not exist\n")
    clear()


# Rewrite content of file
def f4(s):
    path_to_file = os.path.join(s, input("Name of the file which you want to add content: "))
    if os.path.exists(path_to_file):
        with open(path_to_file, mode = 'w') as file:
            print("You can write new content here!")
            print("If you want to finish, just press [ENTER] in empty line")

            content = input("\n")
            while content != "":
                file.write(f"{content}\n")
                content = input()
            print("File succefully edited\n")

    else:
        print("Error, file does not exist\n")
    clear()

def f5(scandir):
     with scandir as items:
        for item in items:
            if item.is_file():
                file = open(item)
                content = file.read()
                print(f"File name: {item.name} _______________________________________") 
                print(content)
                file.close()

# MAIN ___________________________________________________________________________

os.system("cls")
s = input("Enter the path to directory: ")
scandir = os.scandir(s)
os.system("cls")
withDir = True

while True:
    if withDir:
        print(Menu_Dir())
        choice = int(input("Choose the function: "))
        os.system("cls")

        if choice == 1:
            d1(s)

        elif choice == 2:
            d2(scandir)

        elif choice == 3:
            d3(scandir)

        elif choice == 4:
            d4(s)

        elif choice == 5:
            d5(s)

        elif choice == 6:
            d6(s)

        elif choice == 7:
            withDir = False

        elif choice == 0:
            print("You've closed the program")
            exit()

        else:
            print("Incorrect command")
    
    if not withDir:
        print(Menu_File())
        choice = int(input("Choose the function: "))
        os.system("cls")

        if choice == 1:
            f1(s)

        elif choice == 2:
            f2(s)

        elif choice == 3:
            f3(s)

        elif choice == 4:
            f4(s)

        elif choice == 5:
            f5(scandir)

        elif choice == 6:
            withDir = True
        
        elif choice == 0:
            exit(0)

        else:
            print("Incorrect command")