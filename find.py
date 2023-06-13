import ConfigManager
import os
import string
import sys
import util
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--root", dest="root", help="provide the root for search")
parser.add_option("-s", "--skip", dest="skipKeys", default="", help="provide the key to filter folder when traverse the folder.")
parser.add_option("-e", "--execUtil", dest="execUtil", help="provide the utile to run for each file.")
parser.add_option("-l", "--log", dest="logProcessing", action="store_true", default=False, help="output the processing folder.")
parser.add_option("--ed", "--executeDir", dest="execUtilDir", help="provide the utile to run for each dir.")
(options, args) = parser.parse_args()

top = options.root
utilExec = options.execUtil
utilDir = options.execUtilDir

cuePath = util.getEnv("CUE")
globalConfig = ConfigManager.ConfigManager(None)
localConfig = ConfigManager.ConfigManager(cuePath)
#search_file_extension=cpp,h

globalFileExtensionList = globalConfig.get("common", "search_file_extension").split(",")
localFileExtensionList = []
try:
    localFileExtensionList = localConfig.get("common", "search_file_extension").split(",")
except:
    pass

skipPathPatterns = []
if not options.skipKeys== "":
    skipPathPatterns = options.skipKeys.split(";")

def shouldSkip(dirPath):
    match = False;
    for key in skipPathPatterns:
        if (util.wildcardMatch(key, dirPath)):
            match = True;
            break;
    return match


def includeInExtensionList(name):
    for ex in globalFileExtensionList:
        if (name.endswith(ex)):
            return True;
    for ex in localFileExtensionList:
        if (name.endswith(ex)):
            return True;
    return False

for root, dirs, files in os.walk(top, topdown=True):
    if (options.logProcessing):
        print("processing folder:%s" % root)
    for name in files:
        if (includeInExtensionList(name)):
            path = os.path.abspath(os.path.join(root, name))
            if os.path.islink(path):
                continue
            if (utilExec):
                replaceCommand = utilExec.replace("{path}", path)
                commandPath = subprocess.call(replaceCommand, shell=True)
            else:
                print(path)
    for name in dirs:
        if (includeInExtensionList(name)):
            path = os.path.abspath(os.path.join(root, name))
            if os.path.islink(path):
                continue
            if (utilDir):
                replaceCommand = utilDir.replace("{path}", path)
                commandPath = subprocess.call(replaceCommand, shell=False)
            else:
                print(path)

    dirs[:] = [dir for dir in dirs if not shouldSkip(os.path.abspath(os.path.join(root, dir)))]
