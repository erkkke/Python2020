# УДАЛЕНИЕ ПАПОК И ФАЙЛОВ
import os
os.remove(path) - deletes files
os.rmdir(path) - удаляет папку если она пуста

# если нужно удалить папку с  содержимым, то:
import shutil
shutil.rmtree(path)

# КОПИРАВАНИЕ ФАЙЛОВ (старый файл не удаляется)
import shutil
scr = "path/to/file.txt" - полный путь до файла
dst = "path/to/destination_dir"
shutil.copy(scr, dst) 

# КОПИРОВАНИЕ ДИРЕКТОРИЙ
shutil.copytree("data", "date_backup")

# MOVING DIRECTORY
shutil.move("dir/", "backup/")

