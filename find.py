import ConfigManager
import os
import string
import sys
import util
import subprocess
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--root", dest="root", help="provide the root for search")
parser.add_option("-e", "--execute", dest="execUtil", help="provide the utile to run for each file.")
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


def includeInExtensionList(name):
    for ex in globalFileExtensionList:
        if (name.endswith(ex)):
            return True;
    for ex in localFileExtensionList:
        if (name.endswith(ex)):
            return True;

for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        if (includeInExtensionList(name)):
            path = os.path.abspath(os.path.join(root, name))
            if (utilExec):
                replaceCommand = string.replace(utilExec, "{path}", path)
                commandPath = subprocess.call(replaceCommand, shell=True)
            else:
                print path
    for name in dirs:
        if (includeInExtensionList(name)):
            path = os.path.abspath(os.path.join(root, name))
            if (utilDir):
                replaceCommand = string.replace(utilDir, "{path}", path)
                commandPath = subprocess.call(replaceCommand, shell=True)
            else:
                print path
