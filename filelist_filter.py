import sys
import util
from optparse import OptionParser
import imp
import os

parser = OptionParser()
parser.add_option("--org", "--org", dest="orgFile", help="provide the orignal file")
parser.add_option("--plugin", "--plugin", dest="plugin", help="provide plugin.")
parser.add_option("--output", "--output", dest="outputFile", help="output file.")
(options, args) = parser.parse_args()

plugin = None
if (os.path.isfile(options.plugin)):
    plugin = imp.load_source('filelist_filter_plugin', options.plugin)
    print("Successed to load filelist_filter_plugin")
else:
    print ("no filelist filter plugin find in project cue:" + options.plugin)

outputFile = open(options.outputFile, 'w')

orgFile = options.orgFile
f = open(orgFile)
lines = f.readlines()
f.close()

for line in lines:
    line = line.strip()
    if ((not plugin) or plugin.filter(line)):
        outputFile.write(line + "\n")
outputFile.close()

