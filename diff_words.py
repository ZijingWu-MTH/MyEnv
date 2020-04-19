from optparse import OptionParser
import os
import shutil
import string
import subprocess
import sys
import time
import util
import ConfigParser
import io
import re
import logging
import re

log = logging.getLogger("fuzzy")


def isSourceCodeFile(name):
    sourceFileExtensions = [".cc", ".h", ".cpp", ".cxx"];
    for ex in sourceFileExtensions:
        if (name.strip().lower().endswith(ex)):
            return True;
    return False;

def getIdentityFromFiles(paths):
    words = set([])
    for path in paths:
        tmp = getIdentitys(path);
        words = words | tmp;
    return words;

def getIdentitys(path):
    regex = r'[A-Za-z][A-Za-z_0-9]*';
    content = util.readSmallFileAsString(path);
    identities = re.findall(regex, content);
    return set(identities)

def getSourceCodes(folder):
    sourceFiles = [];
    tmpFiles = util.getFilesInFolder(folder);
    for sourceFile in tmpFiles:
        if (isSourceCodeFile(sourceFile)):
            sourceFiles = sourceFiles + [sourceFile];
    return sourceFiles;

if __name__ == '__main__':
    print" usage: python diff_words.py -a folder1 -b folder2"
    parser = OptionParser()
    parser.add_option("-a", "--aFolder", dest="aFolder", help="provide the folder for search source code 1.")
    parser.add_option("-b", "--bFolder", dest="bFolder", help="provide the folder for search source code 2.")

    (options, args) = parser.parse_args()
    if (not options.aFolder or not options.bFolder):
        print " Please provide two folder for search code by -a and -b."
        sys.exit(0)

    aSrcFiles = getSourceCodes(options.aFolder);
    bSrcFiles = getSourceCodes(options.bFolder);

    aIdentities = getIdentityFromFiles(aSrcFiles);
    bIdentities = getIdentityFromFiles(bSrcFiles);
    print "------New word-------:\n";
    for identity in (bIdentities - aIdentities):
       print identity + "\n" 
    print "------Old word-------:\n";
    for identity in (aIdentities - bIdentities):
       print identity + "\n" 
    
        

    
