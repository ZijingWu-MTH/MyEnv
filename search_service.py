import sys
import util
import os
import subprocess

if (len(sys.argv) < 2):
    print "Please give the text for search."
    sys.exit()
text = sys.argv[1]

pathname = os.environ.get("ROOT")
os.chdir(pathname)
platformName = util.getPlatformName()
if (platformName == "win32"):
    command = ["nani", text]
    subprocess.call(command)
else:
    #filePaths = open("filelist.filtered").readlines()
    queryStr = unicode(text, "utf-8")
    rootPath = os.environ.get("ROOT")
    indexDir = os.path.join(rootPath, "_indexdir_")
    filePaths = util.whooshSearch(queryStr, indexDir)
    for filePath in filePaths:
        filePath = filePath.strip()
        if (not os.path.isfile(filePath)):
            continue
        #print "find in " + filePath
        command = ["grep", "-i", "-H", "-n", text, filePath]
        #print command
        subprocess.call(command)
