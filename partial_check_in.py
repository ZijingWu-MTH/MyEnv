import sys
import shutil
import re
import util
import os
import subprocess
sys.path.append(os.environ.get('RPK_SOURCE'))
import merge2

def IsIgnoreBlock(lines):
    skipMark1 = "skip check-in"
    skipMark2 = "skip checkin"
    for line in lines:
        if (line.lower().find(skipMark1) >= 0 or line.lower().find(skipMark2) >= 0):
            return True
    return False

def getFileList():
    status = subprocess.check_output(["svn", "status"])
    lines = status.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if (line.find("M ") == 0):
            line = line[1:]
            line = line.strip()
            result = result + [line]
    return result

def getNeedHandleFile(changedFiles):
    result = []
    for path in changedFiles:
        if (not os.path.isfile(path)):
            continue
        lines = file(path, 'rb').readlines()
        if(IsIgnoreBlock(lines)):
            result = result + [path]
    return result


def partialRevert(orignalFilePath, changedFilePath, targetFilePath):
    changedFile = file(changedFilePath, 'rb').readlines()
    base = file(orignalFilePath, 'rb').readlines()
    m2 = merge2.Merge2(base, changedFile)
    result = []
    for group in m2.merge_struct(True):
        if len(group) == 1:
            lines = group[0]
            result = result + lines
        else:
            aLines = group[0]
            bLines = group[1]
            # if there is skip mark in the changed file, 
            # than we using the first file block, 
            # else using the changed file.
            if (IsIgnoreBlock(bLines)):
                result = result + aLines
            else:
                result = result + bLines

    outputFileFH = open(targetFilePath, "w")
    for item in result:
        outputFileFH.write(item)
    outputFileFH.close()

def handle():
    allChangedFiles = getFileList();
    files = getNeedHandleFile(allChangedFiles)
    for path in files:
        changedFilePath = path + ".partial_check_in.changed"
        shutil.copyfile(path, changedFilePath)
        subprocess.check_call(["svn", "revert", path])
        partialRevert(path, changedFilePath, path)
    return files

def copyback(files):
    for path in files:
        changedFilePath = path + ".partial_check_in.changed"
        shutil.copyfile(path, path + ".partial_check_in.before_check_in")
        shutil.copyfile(changedFilePath, path)

files = handle()
subprocess.call(["svn", "commit"])
copyback(files)
