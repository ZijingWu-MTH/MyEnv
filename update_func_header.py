import sys
import shutil
import time
import datetime
import os
import util
import string
from sets import Set

filePath = sys.argv[1]
remove = (sys.argv[2] == "remove")
lineNum = (int)(sys.argv[3])

def funcHeaderSameObjective(func1, func2):
    func1 = func1.strip().replace(" ", "")
    func1 = func1.replace("\t", "")
    func1 = func1.replace("\r", "")
    func1 = func1.replace("\n", "")
    func2 = func2.strip().replace(" ", "")
    func2 = func2.replace("\t", "")
    func2 = func2.replace("\r", "")
    func2 = func2.replace("\n", "")

    return (func1 == func2 or
        func1 == func2 + ";" or
        func1 + ";" == func2)

def scoreOfLikly(words1, words2):
    wordsSet1 = Set(words1)
    wordsSet2 = Set(words2)
    same = wordsSet1.intersection(wordsSet2)
    diff = wordsSet1.symmetric_difference(wordsSet2)
    return 2 * len(same) - len(diff);

# an simple algorithm to find the most likely
def findMostLiklyLine(target, lines):
    tokens1 = util.tokenize(target)
    tokenWords1 = [t.value for t in tokens1]
    largetstScore = -1000000
    result = None
    for line in lines:
        tokens2 = util.tokenize(line)
        tokenWords2 = [t.value for t in tokens2]
        score = scoreOfLikly(tokenWords1, tokenWords2)
        if (score > largetstScore):
            largetstScore = score;
            result = line
    return result
        

def findHeaderCPP(filePath, lineNum):
    excludeKeyword = {"while", "foreach", "ifelse", "if else", "for", "if", "else", "try", "catch", "case", "switch"}
    header = None;
    className = None;
    lines = file(filePath, 'rt').readlines()
    index = lineNum
    while(index > 0):
        line = lines[index]
        stripLine = line.strip()
        lastLine = None
        if (index + 1 < len(lines)):
            lastLine = lines[index + 1]
        index = index - 1
        
        if (header == None and stripLine.find("(") >= 0 and not util.containsAny(stripLine, excludeKeyword) and lastLine != None and lastLine.strip() == "{"):
            header = line;
            print "find header in cpp:" + header
            break;
    if (header == None):
        return (None, None)
    tokens = util.tokenize(line)
    candidateClassName = None
    for token in tokens:
        if (token.value == "::"):
            className = candidateClassName
        candidateClassName = token.value;
    return (header, className)

def findHeaderObjectiveC(filePath, lineNum):
    header = None;
    className = None;
    lines = file(filePath, 'rt').readlines()
    index = lineNum
    while(index > 0):
        line = lines[index]
        index = index - 1
        if (header == None and line.strip().find("-") == 0):
            header = line;
        #@implementation RPDAppDelegate
        if (className == None and line.find("@implementation") >= 0):
            className = line.replace("@implementation", "").strip();
    return (header, className)

def updateFuncHeaderCPP(headerFile, funcHeader, className):
    if (not os.path.exists(headerFile)):
        print "not find header file"
        return False

    #find class begin and end.
    lines = file(headerFile, 'rt').readlines()
    index = 0
    classStartLine = 0;
    classEndLine = len(lines)

    funcHeader = string.replace(funcHeader, className + "::", "")
    print "After remove class name:" + funcHeader

    targetLine = findMostLiklyLine(funcHeader, lines)
    print "Going to replace this line:" + targetLine

    isStatic = (targetLine.find("static") >= 0)
    if (isStatic):
        funcHeader = "static " + funcHeader

    isVirtual = (targetLine.find("virtual") >= 0)
    if (isVirtual):
        funcHeader = "virtual " + funcHeader


    if (targetLine != None):
        # find insert line
        index = classStartLine
        insertLine = classEndLine - 1;
        while(index <= classEndLine):
            line = lines[index]
            if (targetLine == line):
                insertLine = index;
                break;
            index = index + 1
        # insert it.
        lines = lines[0:insertLine] + [funcHeader + ";\n"] + lines[insertLine + 1 : len(lines)]
    else:
        results = []
        results = results + lines[0:classStartLine];
        index = classStartLine
        while (index <= classEndLine):
            line = lines[index]
            if (not funcHeaderSameObjective(line, funcHeader)):
                results = results + [line]
            index = index + 1
        results = results + lines[classEndLine + 1: len(lines)];
        lines = results
        
    fo = open(headerFile, "w")
    fo.writelines(lines)
    fo.close()
    return True


def updateFuncHeaderObjectiveC(headerFile, funcHeader, className, remove):
    if (not os.path.exists(headerFile)):
        print "not find header file"
        return False

    #find class begin and end.
    lines = file(headerFile, 'rt').readlines()
    index = 0
    classStartLine = -1
    classEndLine = -1;
    while(index < len(lines)):
        line = lines[index]
        if ((line.find("@interface") >= 0 or line.find("@class") >=0 ) and line.find(className) >= 0):
            print "find class begin:" + line
            classStartLine = index
        if (classStartLine >= 0 and line.find("@end") >= 0):
            print "find class end:" + line
            classEndLine = index
        index = index + 1
    
    if (classStartLine == -1 or classEndLine == -1):
        print "not find class start and end"
        return False

    if (not remove):
        index = classStartLine
        while (index <= classEndLine):
            line = lines[index]
            if (funcHeaderSameObjective(line, funcHeader)):
                print "skip because of header has been found in header."
                return False
            index = index + 1

        # find insert line
        index = classStartLine
        insertLine = classEndLine - 1;
        while(index <= classEndLine):
            line = lines[index]
            if (line.find("-") >= 0):
                insertLine = index;
                break;
            index = index + 1

        # insert it.
        lines = lines[0:insertLine] + [funcHeader + ";\n"] + lines[insertLine : len(lines)]
    else:
        results = []
        results = results + lines[0:classStartLine];
        index = classStartLine
        while (index <= classEndLine):
            line = lines[index]
            if (not funcHeaderSameObjective(line, funcHeader)):
                results = results + [line]
            index = index + 1
        results = results + lines[classEndLine + 1: len(lines)];
        lines = results
        
    fo = open(headerFile, "w")
    fo.writelines(lines)
    fo.close()
    return True


if (filePath.endswith('.mm') or filePath.endswith('.m')):
    (funcHeader, className) = findHeaderObjectiveC(filePath, lineNum)
if (filePath.endswith('.cpp') or filePath.endswith('.c')):
    (funcHeader, className) = findHeaderCPP(filePath, lineNum)

if (not funcHeader):
    print "The function header not found."
    sys.exit(0)

funcHeader = funcHeader.strip()
headerFile = filePath
headerFile = headerFile.replace(".mm", ".h")
headerFile = headerFile.replace(".m", ".h")
headerFile = headerFile.replace(".cpp", ".h")
headerFile = headerFile.replace(".c", ".h")

if (not os.path.exists(headerFile)):
    print "header file not found."
    sys.exit(0)


if (filePath.endswith('.mm') or filePath.endswith('.m')):
    updateFuncHeaderObjectiveC(headerFile, funcHeader, className, remove)
if (filePath.endswith('.cpp') or filePath.endswith('.c')):
    updateFuncHeaderCPP(headerFile, funcHeader, className)
shutil.copyfile(headerFile, headerFile + ".bak")




