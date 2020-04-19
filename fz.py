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

def reverseUniqueMap(mapData):
    result = dict();
    for key in mapData:
        value = mapData[key];
        result[value] = key;
    return result;
        
        
def loadMapFile(path):
    lines = util.getLinesWithoutLineEnd(path);
    wordsMap = dict({});    
    keySet = set([])
    valueSet = set([])
    for line in lines:
        words = line.split(":")
        if (len(words) == 2):
            wordsMap[words[0].strip()] = words[1].strip();

            if (words[0].strip() not in keySet):
                keySet = keySet | set([words[0].strip()]);
            else:
                raise Exception("Invalid map file. Key exits twice:" + words[0].strip());
            if (words[1].strip() not in valueSet):
                valueSet = valueSet | set([words[1].strip()]);
            else:
                raise Exception("Invalid map file. Value exits twice:" + words[1].strip())

    return wordsMap

def replaceFilesContent(paths, wordsMap):
    for path in paths:
        print "Process file:" + path
        replaceFileContent(path, wordsMap);

def replaceFileContent(path, wordsMap):
    content = util.readSmallFileAsString(path)
    for key in wordsMap:
        value = wordsMap[key]
        pattern = "\\b" + key + "\\b"
        content = re.sub(pattern, value, content)
    
    if (path and os.path.exists(path) and os.path.isfile(path)):
        newFileName = path + "." + util.id_generator(6);
        print "backup the file to :" + newFileName
        shutil.copyfile(path, newFileName)
    util.writeSmallFileAsString(path, content);
    return content

def getSourceCodes(folder):
    sourceFiles = [];
    tmpFiles = util.getFilesInFolder(folder);
    for sourceFile in tmpFiles:
        if (isSourceCodeFile(sourceFile)):
            sourceFiles = sourceFiles + [sourceFile];
    return sourceFiles;

if __name__ == '__main__':
    print" usage: python fz.py -f codeFolder -r True -m mapFile -p password"
    parser = OptionParser()
    parser.add_option("-f", "--folder", dest="folder", help="provide the folder for search source code.")
    parser.add_option("-r", "--replace", dest="replaceVariable", help="replace the variables.")
    parser.add_option("-m", "--map_file", dest="mapFile", help="Give the encrypt file.")
    parser.add_option("-p", "--password", dest="password", help="The password of the encrypt file.")


    (options, args) = parser.parse_args()

    if (options.mapFile and os.path.exists(options.mapFile) and os.path.isfile(options.mapFile)):
        newFileName = options.mapFile + "." + util.id_generator(6);
        print "backup the map file to :" + newFileName
        shutil.copyfile(options.mapFile, newFileName)
        
    top = options.folder;
    replaceVariable = options.replaceVariable;

    sourceFiles = getSourceCodes(options.folder);

    if (replaceVariable.lower() == "true"):
        wordsMaps = loadMapFile(options.mapFile);
        replaceFilesContent(sourceFiles, wordsMaps);
    else:
        wordsMaps = loadMapFile(options.mapFile);
        wordsMaps = reverseUniqueMap(wordsMaps);
        replaceFilesContent(sourceFiles, wordsMaps);
