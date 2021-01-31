import os
from datetime import datetime
s = os.getcwd()
a = os.scandir(s)

def d7(scandir):
    for item in scandir:
        information = item.stat()
        date = datetime.utcfromtimestamp(information.st_mtime)
        format_date = date.strftime("%d %b %y")
        print(item.name, format_date)

d7(a)