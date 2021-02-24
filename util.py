import sys
import os
import collections
import re

#sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/whoosh/src'))
#from whoosh.index import create_in
#from whoosh.fields import *
#from whoosh.qparser import QueryParser
#from whoosh.index import open_dir
#from whoosh.query import *

#sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/slowaes/python'))
#import aes

try:
    import _winreg
except ImportError:
    #make no compile error happen. 
    dumpvar = 1    
     
import urlparse
import posixpath
import os.path
import string
import shutil
import subprocess;
import tempfile
import re
import random
import zipfile
from xml.dom.minidom import parseString
from xml.dom.minidom import Document
import logging
import logging.handlers

def getLogPath():
    homeDir = os.path.expanduser('~')
    logfile = os.path.join(homeDir, "rpklog.log")
    return logfile

def initLog():
    logger = logging.getLogger()
    logfile = getLogPath()
    fileLogHandler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fileLogHandler.setFormatter(formatter)
    logger.addHandler(fileLogHandler)
    logger.setLevel(logging.NOTSET)
    return logger
    
def relurl(target,base): 
    base=urlparse.urlparse(base) 
    target=urlparse.urlparse(target) 
    if base.netloc != target.netloc: 
        raise ValueError('target and base netlocs do not match') 
    base_dir='.'+ base.path
    target='.'+ target.path 
    return posixpath.relpath(target, start=base_dir) 

def isIgnoredFileDirName(name):
    if (name == ".svn" or name == ".hg"):
        return True
    return False
    

def normalizePath(path):
    if (os.sep == "\\"):
        path = path.replace("/", os.sep);
    elif (os.sep == "/"):
        path = path.replace("\\", os.sep);
    return path

def getPlatformName():
    if (sys.platform.startswith('win32')):
        return "win32"
    elif (sys.platform.startswith('darwin')):
        return "mac"
    elif (sys.platform.startswith('linux')):
        return "linux"
    return None

def pause():
    try:
        if (sys.platform.startswith('win32')):
            os.system('pause')  #windows, doesn't require enter 
        elif (sys.platform.startswith('darwin')):
            os.system('read -p "Press any key to continue"') #linux
        elif (sys.platform.startswith('linux')):
            os.system('read -p "Press any key to continue"') #linux
    except Exception: 
        logging.exception("Exception happen when try to pause")

def makeFileName(fileName):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits) 
    fileName = ''.join(c for c in fileName if c in valid_chars) 
    fileName = fileName.strip()
    return fileName

def getTempFolder():
    tempFolderRoot = getEnv("RPK_TEMPDIR")
    if (tempFolderRoot != None):
        randomId = id_generator()
        while True:
            tempFolderPath = os.path.join(tempFolderRoot, randomId)
            if (not os.path.exists(tempFolderPath)):
                os.makedirs(tempFolderPath)
                return tempFolderPath
    tempFolderPath = tempfile.mkdtemp()
    return tempFolderPath

def getEnv(name):
    try:
        return os.environ[name]
    except KeyError:
        return None

def id_generator(size=6, chars=string.ascii_uppercase + string.digits): 
    return ''.join(random.choice(chars) for x in range(size)) 

def safeCopyFile(srcFilePath, dstFilePath):
    tmpFileNameSuffix = id_generator(6)
    if (os.path.isfile(dstFilePath)):
        #TODO by zijwu we may need to check tempFileNameSuffix exist or not,
        #But the possiblity is very very small.
        shutil.copyfile(dstFilePath, dstFilePath + tmpFileNameSuffix)
        os.unlink(dstFilePath)
    shutil.copyfile(srcFilePath, dstFilePath)
    if (os.path.isfile(dstFilePath + tmpFileNameSuffix)):
        os.unlink(dstFilePath + tmpFileNameSuffix)

def getCurrentUser():
    if (sys.platform.startswith('win32')):
        return os.getenv('USERNAME') 
    else:
        return os.getlogin()

def getLinesWithoutLineEnd(filePath):
    lines = file(filePath, 'rt').readlines()
    newLines = []
    for line in lines:
        line = line.rstrip("\n")
        newLines = newLines + [line]
    return newLines

def concateLines(lines):
    line = ""
    for tmp in lines:
        if (line):
            line = line + "\n" + tmp
        else:
            line = tmp
    return line

def readSmallFileAsString(filePath):
    with open(filePath, 'r') as content_file:
        return content_file.read();
    return None;

def writeSmallFileAsString(filePath, content):
    outfile = open(filePath, 'w')
    outfile.write(content)
    outfile.close()

def removeSpace(strings):
    result = []
    for item in strings:
        item = item.strip()
        result = result + [item]
    return result

def filterEmptyString(strings):
    result = []
    for item in strings:
        if (item == ""):
            continue;
        result = result + [item]
    return result

def checkAppExistOnMacAndLinux(commandName):
    try:
        commandPath = subprocess.check_call(["which", commandName])
        if (commandPath and commandPath.strip() != ""):
            return False
        return True
    except subprocess.CalledProcessError:
        logging.exception("'which' command throw exception")
        return False

def getDiffTool():
    diffTool = os.getenv("RPK_DIFF")
    if diffTool != None :
        return [diffTool]

    if (sys.platform.startswith('win32')):
        #We first detect the beyond compare
        filePath = searchBeyondCompare()
        if (filePath != None):
            return [filePath]
        filePath = searchWinMerge()
        if (filePath != None):
            return [filePath]
        #We print the msg for set RPK_DIFF if we doesn't have the user doesn't have compare tool
        diffTool = os.path.join(os.path.dirname(sys.argv[0]), "DiffTools\\windiff.exe")
        print "You can set RPK_DIFF environment variable to customize it"
        return [diffTool]
    elif (sys.platform.startswith('darwin')):
        exist = checkAppExistOnMacAndLinux("opendiff")
        if (exist):
            return ["opendiff"]
        print "You can set RPK_DIFF environment variable to customize it"
    elif (sys.platform.startswith('linux')):
        exist = checkAppExistOnMacAndLinux("meld")
        if (exist):
            return ["meld"]
        exist = checkAppExistOnMacAndLinux("kdiff3")
        if (exist):
            return ["kdiff3"]
        print "You can set RPK_DIFF environment variable to customize it"
    else:
        raise error.PlatformNotSupported(error.Msg.platformNotSupportedError)

    # At last for Mac and Linux we using vim + DirDiff
    if (sys.platform.startswith('darwin') or sys.platform.startswith('linux')):
        exist = checkAppExistOnMacAndLinux("vim")
        if (exist):
            loadDirDiffPath = os.path.join(os.path.dirname(sys.argv[0]), "LoadDirDiff.vim")
            return ["vim", "-S", loadDirDiffPath]
    raise error.NoDiffTool(error.Msg.noDiffToolError)

def searchNotepadPlusPlus():
    value = getRegValue( _winreg.HKEY_CURRENT_USER, "Software\\Notepad++", None)
    if (value != None):
        filePath = os.path.join(value, "notepad++.exe")
        if (os.path.isfile(filePath)):
            return filePath

    value = getRegValue( _winreg.HKEY_LOCAL_MACHINE, "Software\\Notepad++", None)
    if (value != None):
        filePath = os.path.join(value, "notepad++.exe")
        if (os.path.isfile(filePath)):
            return filePath
    return None
    

#Only valid on windows
def searchWinMerge():
    value = getRegValue( _winreg.HKEY_CURRENT_USER, "Software\\Thingamahoochie\\WinMerge", "Executable")
    if (value != None and os.path.isfile(value)):
        return value

    value = getRegValue( _winreg.HKEY_LOCAL_MACHINE, "Software\\Thingamahoochie\\WinMerge", "Executable")
    if (value != None and os.path.isfile(value)):
        return value
    

def getRegValue(rootKey, path, name):
    try:
        pathKey = _winreg.OpenKey(rootKey, path)
        val, valType = _winreg.QueryValueEx(pathKey, name)
        _winreg.CloseKey(pathKey)
        return val;
    except WindowsError, e:
        return None

#Only valid on windows, current it will detect the Beyond compare 1/2/3, please make 
#sure the speed of this function. because it will be used if user doesn't have set PRK_DIFF, 
#which will be high hit rate.
def searchBeyondCompare():
    #We first check the beyond compare 3 instead of beyond compare 2. We doesn't support Beyond compare 1, which is too old build.
    value = getRegValue( _winreg.HKEY_CURRENT_USER, "Software\\Scooter Software\\Beyond Compare3", "ExePath")
    if (value != None and os.path.isfile(value)):
        return value

    value = getRegValue( _winreg.HKEY_LOCAL_MACHINE, "Software\\Scooter Software\\Beyond Compare3", "ExePath")
    if (value != None and os.path.isfile(value)):
        return value

    value = getRegValue( _winreg.HKEY_CURRENT_USER, "Software\\Scooter Software\\Beyond Compare", "ExePath")
    if (value != None and os.path.isfile(value)):
        return value

    value = getRegValue( _winreg.HKEY_LOCAL_MACHINE, "Software\\Scooter Software\\Beyond Compare", "ExePath")
    if (value != None and os.path.isfile(value)):
        return value
    return None

def unzipFileIntoFolder(filename, outdir, patternStr = None, callback = None):
    #TODO: should we create a different folder?
    if (patternStr == None):
        patternStr = ".*"
    # we ignore case, let make it sensative, if we need later.
    pattern = re.compile(patternStr, re.I)
    if (not os.path.exists(outdir)):
        os.makedirs(outdir)
    try:
        zfobj = zipfile.ZipFile(filename)
    except zipfile.BadZipfile, e:
        raise error.InvalidRPKFileError(error.Msg.invalidRPKFileError)
    for name in zfobj.namelist():
        if (not re.match(pattern, name)):
            continue
        if name.endswith('/'):
            if (not os.path.exists(os.path.join(outdir, name))):
                os.makedirs(os.path.join(outdir, name))
        else:
            outfilename = os.path.join(outdir, name)
            dirname = os.path.dirname(outfilename)
            if ( not os.path.exists(dirname)):
                os.makedirs(dirname)
            outfile = open(os.path.join(outdir, name), 'wb+')
            outfile.write(zfobj.read(name))
            outfile.close()
        if (callback != None):
            callback(name, os.path.join(outdir, name))
            
def removeFolder(folder):
    if (not os.path.exists(folder)):
        return
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            else:
                removeFolder(file_path)
        except Exception, e:
            print e
    os.rmdir(folder)

#return 0 for false, 1 for same, 2 for subfolder, user can check if return 
#result is > 0 if just care bool value.
def isSameOrSubFolder(parentPath, path):
    parentPath = os.path.normcase(os.path.normpath(parentPath))
    path = os.path.normcase(os.path.normpath(path))
    if (parentPath == path):
        return 1
    while(parentPath != path):
        newPath = os.path.normpath(os.path.dirname(path))
        # got the top, which doesn't dirname doesn't do any change.
        if (newPath == path):
            return 0
        path = newPath
    return 2

# this require absolute path
def checkCodeRepositeType(filePath):
    if (findGitRoots(filePath)):
        return "git"
    if (len(findSVNRoots(filePath)) > 0):
        return "svn"
    raise Exception("Cannot determinate the source code depot type.")
    return "unknown"

# this require absolute path
def findGitRoots(currentFolder):
    while (currentFolder != ""):
        if os.path.exists(os.path.join(currentFolder, ".git")):
            return currentFolder
        dirPath = os.path.dirname(currentFolder)
        #do we still need to take care case
        if (dirPath.lower() == currentFolder.lower()):
            break;
        currentFolder = dirPath
    return None

# this require absolute path
def findSVNRoots(currentFolder):
    result = [] 
    possibleSvnRoot = None
    possibleSvnRootUrl = None
    while (currentFolder != ""):
        if os.path.exists(os.path.join(currentFolder, ".svn")):
            (rootUrl, currentFolderUrl) = svnInfo(currentFolder)
            if (possibleSvnRootUrl != None and possibleSvnRoot != None):
                logging.debug("Handle possible svn root url %s and possible svn root path %s", possibleSvnRootUrl, possibleSvnRoot)
                logging.debug("current svn root url %s and possible svn root path %s", currentFolderUrl, currentFolder)
                urlDelta = relurl(currentFolderUrl, possibleSvnRootUrl)
                pathDelta = posixpath.relpath(currentFolder, possibleSvnRoot)
                logging.debug("urlDelta %s, pathDelta %s", urlDelta, pathDelta)
                if (urlDelta.replace("\\", "/").strip("/").lower() != pathDelta.replace("\\", "/").strip("/").lower()):
                    result = result + [possibleSvnRoot]
            possibleSvnRootUrl = currentFolderUrl
            possibleSvnRoot = currentFolder
        dirPath = os.path.dirname(currentFolder)
        #do we still need to take care case
        if (dirPath.lower() == currentFolder.lower()):
            break;
        currentFolder = dirPath

    if (possibleSvnRoot != None):
        result = result + [possibleSvnRoot]
    return result

def isNumber(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def askUserSelectRootFolder(svnFolders):
    print "You have more than one SVN root, which one are you want to use:" 
    index = 0 
    for item in svnFolders:
        print str(index) + ". " + item
        index = index + 1

    selectIndex = -2
    while(not (selectIndex == -1 or selectIndex >= 0 and selectIndex <= len(svnFolders) - 1)):
        userInputStr = raw_input("Please select the svn root index, -1 for abort:")
        if (isNumber(userInputStr)):
            selectIndex = int(userInputStr)
    
    if (selectIndex == -1):
        return None
    return svnFolders[selectIndex]

def file_iterator(input_file, readsize=32768):
    while True:
        b = input_file.read(readsize)
        if len(b) == 0:
            break
        yield b

def svnInfo(folderPath):
    if (folderPath == None):
        folderPath = os.getcwd()
    try:
        infoXml = subprocess.check_output(["svn", "info", "--xml"], cwd=folderPath)
    except OSError:
        raise error.NoSvnCmdError(error.Msg.noSvnCmdError)
    statusDom = parseString(infoXml)
    rootInfoElements = statusDom.getElementsByTagName("root")
    workingPathInfoElments = statusDom.getElementsByTagName("url")
    if (len(rootInfoElements) < 1 or len(workingPathInfoElments) < 1):
        raise Exception("cannot found the working space info.")
    if (len(rootInfoElements[0].childNodes) < 1 or len(workingPathInfoElments[0].childNodes) < 1):
        raise Exception("cannot found the working space info.")
    rootUrl = rootInfoElements[0].childNodes[0].nodeValue
    workingPathInfoPath = workingPathInfoElments[0].childNodes[0].nodeValue
    return (rootUrl, workingPathInfoPath)

#def whooshSearch(queryStr, indexDir):
#    resultPaths = []
#    ix = open_dir(indexDir)
#    with ix.searcher() as searcher:
#        query = QueryParser("content", ix.schema).parse(queryStr)
#        results = searcher.search(query, limit=5000)
#        for result in results:
#            resultPaths = resultPaths + [result["path"]]
#    return resultPaths

def containsAny(str, keyList):
    for key in keyList:
        if (str.find(key) >= 0):
            return key
    return None

def filterList(itemList, patternStr):
    result = [] 
    pattern = re.compile(patternStr, re.I)
    for item in itemList:
        if (not re.match(pattern, item)):
            continue
        result = result + [item]
    return result

def getFilesInFolder(folder):
    result = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            result = result + [os.path.join(root, name)]
    return result

Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
class ComparedToken(Token):
    def __hash__(self):
        return self.value.__hash__()
    def __eq__(self, other):
        return self.value.__eq__(other.value)

def tokenize(s):
    keywords = {'if', 'then', 'else', 'for', 'break', 'continue', 'return'}
    token_specification = [
        ('NUMBER',  r'\d+(\.\d*)?'), # Integer or decimal number
        ('ASSIGN',  r':='),          # Assignment operator
        ('END',     r';'),           # Statement terminator
        ('ID',      r'[A-Za-z][A-Za-z_0-9]*'),   # Identifiers
        ('OP',      r'[+*\/\-]'),    # Arithmetic operators
        ('DOUBLE_COLON', r'::'),     # double colon
        ('NEWLINE', r'\n'),          # Line endings
        ('SKIP',    r'[ \t]'),       # Skip over spaces and tabs
        ('UNEXPECTED', r'.'),       # unexpected
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line = 1
    pos = line_start = 0
    mo = get_token(s)
    while mo is not None:
        typ = mo.lastgroup
        if typ == 'NEWLINE':
            line_start = pos
            line += 1
        elif typ != 'SKIP':
            val = mo.group(typ)
            if typ == 'ID' and val in keywords:
                typ = val
            yield ComparedToken(typ, val, line, mo.start()-line_start)
        pos = mo.end()
        mo = get_token(s, pos)
    if pos != len(s):
        raise RuntimeError('Unexpected character %r on line %d' %(s[pos], line))

def getHeaderFileBaseOnSource(filePath):
    m = re.match("(.*)\.cpp$", filePath)
    if (m):
        return m.group(1) + ".h"
    return ""
