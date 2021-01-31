import os
s = os.getcwd()
a = os.scandir(s)

from datetime import datetime
def convert_time(time):
    date = datetime.utcfromtimestamp(time)
    format_date = date.strftime("%d %b %y")
    return format_date

for item in a:
    info = item.stat()
    print(item.name, convert_time(info.st_mtime))


def info(a):
    for item in a:
        information = item.stat()
        date = datetime.utcfromtimestamp(information.st_mtime)
        format_date = date.strftime("%d %b %y")
        print(item.name, format_date)
