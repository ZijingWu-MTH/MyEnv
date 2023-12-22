import sys
import re
import util
import os
import subprocess

def getFolderPath(path):
    if (os.path.isfile(path)):
        return os.path.dirname(path)
    return path

def findParentItem(path, keyPattern):
    result = []
    while(True):
        name = os.path.basename(path)
        newPath = os.path.dirname(path)
        if (newPath == path):
            return result;
        if (re.match(keyPattern, name)):
            result = result + [path]
        path = newPath
    return result
    

def findSubItem(dir, keyPattern, includeFile, includeFolder):
    result = []
    for root, dirs, files in os.walk(dir, True):
        if (includeFile):
            for name in files:
                if (re.match(keyPattern, name)):
                    result = result + [os.path.join(root, name)]
        if (includeFolder):
            for name in dirs:
                if (re.match(keyPattern, name)):
                    result = result + [os.path.join(root, name)]
        
        prunedDirs = [x for x in dirs if not util.isIgnoredFileDirName(x)]
        dirs[:] = prunedDirs
        depth = root.count(os.path.sep) - dir.count(os.path.sep)
        if depth >= 12:
            # We're currently two directories in, so all subdirs have depth 10
            dirs[:] = [] # Don't recurse any deeper'
    return result

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-e", "--execUtil", dest="execUtil", help="the command template to execute.")
parser.add_option("-f", "--includeFile", dest="includeFile", action="store_true", default = False, help="include the file.")
parser.add_option("-d", "--includeFolder", dest="includeFolder", action="store_true", default = False, help="include the folder.")
(options, args) = parser.parse_args()

if (len(sys.argv) < 4):
    print("Please give the text for search.")
    sys.exit()
utilExec = options.execUtil
key = sys.argv[1]
direction = sys.argv[2]
shellScriptPath = sys.argv[3]

output = open(shellScriptPath, "w")

key = key.replace(".", "\.")
key = key.replace("?", ".?")
key = key.replace("*", ".*")

if (direction == "up"):
    result = findParentItem(os.getcwd(), key)
else:
    result = findSubItem(os.getcwd(), key, options.includeFile, options.includeFolder)

# If there is exactly match, then we using the exactly match.
if (len(result) > 1):
    filteredResult = []
    for item in result:
        if (os.path.basename(item) == result):
            filteredResult = filteredResult + [item]
    if (len(filteredResult) == 1):
        result = filteredResult


path = "."
if (len(result) == 0):
    print("Cannot find the path.")
elif (len(result) > 1):
    print("There are multiple path match the pattern, and cannot choose the one exactly matches:")
    index = 0
    for item in result:
        print(str(index) + ": " + item)
        index = index + 1

    userInputStr = input("Please select the one you want goto. Press Enter to abort:")
    if (util.isNumber(userInputStr)):
        selectIndex = int(userInputStr)
        path = result[selectIndex]
else:

    path = result[0]

folder = getFolderPath(path)

replaceCommand = utilExec
replaceCommand = replaceCommand.replace("{folder}", folder)
replaceCommand = replaceCommand.replace("{path}", path)
output.write(replaceCommand)

output.close()
