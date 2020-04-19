import sys
import util
import os
import subprocess
import codecs
import re;

if (len(sys.argv) < 2):
    print "Please give the change list number and path as the parameter."
    sys.exit(0)

changeNum = int(sys.argv[1])
path = sys.argv[2]
path = os.path.abspath(path)

dirPath = path
if (os.path.isfile(path)):
    dirPath = os.path.dirname(path)

svnInfoOutput = subprocess.check_output(["svn", "info", path])

m = re.search("URL: (http.*)", svnInfoOutput)
svnUrl = m.group(1)
print "The server url is %s" % (svnUrl)
subprocess.check_call(["svn", "merge", "-r", "%d:%d" % (changeNum, changeNum - 1), svnUrl, path])

