import subprocess
import sys
import time
import datetime
import os


pathname = os.path.expandvars("%CUE%")

day = 0
if (len(sys.argv) > 1):
    day = int(sys.argv[1])

paths = file(os.path.join(os.path.abspath(pathname), "monitor_folder_list")).readlines()
today = datetime.date.today() + datetime.timedelta(day)
for path in paths:
    path = os.path.expandvars(path.strip())
    os.chdir(path)
    tomorrow = datetime.date.today() + datetime.timedelta(days=1) + datetime.timedelta(day)
    text = subprocess.check_output("svn log -r {%s}:{%s}" % (today, tomorrow))
    print (("svn log -r {%s}:{%s}" % (today, tomorrow)))
    print text

