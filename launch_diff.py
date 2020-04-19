import subprocess
import sys
import time
import datetime
import os
import util

filePath = sys.argv[1]
versionNum = None 
if (len(sys.argv) > 2):
    versionNum = int(sys.argv[2])

dirPath = os.path.dirname(filePath)
fileName = os.path.basename(filePath)

#firstly change the dir, if it is not empty because the filePath is just a file name
if (not dirPath and not dirPath == ""):
    os.chdir(dirPath)

platformName = util.getPlatformName()

if (platformName == "win32"):
    shellName = "svnwindiff.bat"
    command = ["start"]
else:
    shellName = "svnwindiff.sh"
    command = []


if (versionNum == None):
    command = command + ["svn", "diff", "--diff-cmd", os.path.join(os.environ["myEnvFolder"], shellName), filePath]
else:
    command = command + ["svn", "diff", "-c", versionNum, "--diff-cmd",  os.path.join(os.environ["myEnvFolder"], shellName), filePath]

print command
subprocess.check_call(command, shell=True)
