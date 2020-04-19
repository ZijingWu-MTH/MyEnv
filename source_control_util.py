import sys
import shutil
import re
import util
import os
import subprocess
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="file", help="provide the file path")
parser.add_option("-a", "--action", dest="action", help="provide the action for this path")
(options, args) = parser.parse_args()

filePath = options.file
filePath = os.path.abspath(filePath)

codeDepotType = util.checkCodeRepositeType(filePath)

if (options.action == "revert_local"):
    if (codeDepotType == "svn"):
        subprocess.check_call(["svn", "revert", filePath]) 
    elif (codeDepotType == "git"):
        subprocess.check_call(["git", "checkout", filePath]) 
    else:
        raise Exception("failed to revert file because of unknown depot type.")

