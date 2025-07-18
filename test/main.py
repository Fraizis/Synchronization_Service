import os
from datetime import datetime

directory = os.path.abspath(os.getcwd())
files = os.listdir(directory)

print(directory)


for i in files:
    time_sec = os.path.getmtime(os.path.join(directory, i))
    get_change_time = datetime.fromtimestamp(time_sec)
    print(i)
    print(get_change_time)

print(files)
