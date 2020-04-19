from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import collections
import re
import traceback
import traceback
import uuid
#import ftp_server
import subprocess
#import telnet_server
import thread
import time
import xml.etree.cElementTree as ET
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../tools/recordtype'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import util
import ConfigManager
from recordtype import recordtype

config = ConfigManager.ConfigManager(None)

def getUUIDFromCrashReport(filePath):
    lines = file(filePath, 'rb').readlines()
    result = None
    appName = None
    for line in lines:
        line = line.replace("&lt;", "<")
        line = line.replace("&gt;", ">")
        print line
        m = re.search(".* <([a-zA-Z0-9]{32})> .*/([^/]*)\.app.*", line)
        if (m == None):
            m = re.search(".* <(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})> .*/([^/]*)\.app", line)
        if (m == None):
            continue
        result = m.group(1)
        appName = m.group(2)
        print appName + " : " + result
        
        break;
    if (not result == None):
        result = result.replace("-", "")
        result = result.lower().strip()
        appName = appName.strip()
    return (result, appName)

def getBuildDownloadConfig(filePath):
    lines = file(filePath, "rb").readlines()
    result = None
    for line in lines:
        line = line.strip()
        if (len(line) > 1):
            return line
    return None

def getUUIDFromMDLSOutput(filePath):
    lines = file(filePath, "rb").readlines()
    result = None
    for line in lines:
        m = re.search("(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})", line)
        if (m == None):
            continue
        result =  m.group(1)
        break;
    if (not result == None):
        result = result.replace("-", "")
        result = result.lower().strip()
    return result

def findBinary(binaryDirPath, uuid, appName):
    mdlsPathPostfix = config.get("crashreport", "mdlsPathPostfix")
    # TODO by zijwu, we actually need more good way to concate them.
    mdlsDirPath = binaryDirPath  + mdlsPathPostfix
    lines = file(os.path.join(mdlsDirPath, "buildlist.txt"), "rb").readlines()
    for buildItem in lines:
        try:
            buildItem = buildItem.strip()
            buildItemPath = os.path.join(mdlsDirPath, buildItem)
            mdlsPath = os.path.join(buildItemPath, "mdls.txt") 
            if (not os.path.isfile(mdlsPath)):
                continue
            mdls_uuid = getUUIDFromMDLSOutput(mdlsPath)
            print mdls_uuid
            if (not (mdls_uuid == None) and mdls_uuid == uuid):
                return buildItem
        except:
            print "find the binary in " + buildItem + " error. Please checkk mdls.txt exist"
            traceback.print_exc()
            pass
    return None

def checkSpotlightFinishedIndex(slashSeparateGUID, appName, binaryFolderName):
    mdScript = "mdfind \"com_apple_xcode_dsym_uuids == " + slashSeparateGUID + "\""
    print mdScript
    result = subprocess.check_output(mdScript, shell=True)
    result = result.strip()
    print "search dsym" + result
    if (len(result) == 0):
        return False

    findBinaryScript1 = "mdfind \"kMDItemContentType == public.unix-executable && kMDItemDisplayName == '%s'\"" % (appName)
    result1 = subprocess.check_output(findBinaryScript1, shell=True)
    result1 = result1.strip()

    findBinaryScript2 = "mdfind \"kMDItemContentType == com.apple.application-bundle && (kMDItemAlternateNames == '%s.app' || kMDItemDisplayName == '%s' || kMDItemDisplayName == '%s.app')\"" % (appName, appName, appName)
    result2 = subprocess.check_output(findBinaryScript2, shell=True)
    result2 = result2.strip()

    print "search unix-executable" + result1
    print "search bundle" + result2
    
    if (result1.find(binaryFolderName) >= 0 or result2.find(binaryFolderName) >= 0):
        return True
    return False

def convertCrashReport(data):
    tempDir = config.get("crashreport", "tempDir")
    if (not os.path.exists(tempDir)):
        os.makedirs(tempDir)
    tempFile = os.path.join(tempDir, util.id_generator(8))
    orignalFile = open(tempFile, "w")
    orignalFile.write(data)
    orignalFile.close()
    path = convert(tempFile)
    if (path == None):
        return None
    resultFile = open(path, "r")
    result = resultFile.read()
    resultFile.close()
    return result

def convert(crashReportPath):
    (crashReportUUID, appName) = getUUIDFromCrashReport(crashReportPath)
    binaryDirs = config.get("crashreport", "binaryPath").split(";")
    binaryDir = None
    for binaryDir in binaryDirs:
        try:
            print "try to find the binary in " + binaryDir
            binaryPath = findBinary(binaryDir, crashReportUUID, appName)
        except:
            print "find binary in " + binaryDir + " error happen. Please check the buildlist.txt and mdls.txt exist."
            traceback.print_exc()
            pass
        if (not binaryPath == None):
            break
    if (binaryPath == None):
        print "Cannot find the binary. Convert failed."
        return None
    buildPath = os.path.join(binaryDir, binaryPath) 
    resultDir = os.path.join(binaryDir, "crashReports")
    if (not os.path.exists(resultDir)):
        os.makedirs(resultDir)
    tempDir = config.get("crashreport", "tempDir")
    if (not os.path.exists(tempDir)):
        os.makedirs(tempDir)
    resultReportId = os.path.join(tempDir, os.path.basename(crashReportPath) + util.id_generator(8))

    # download the build.
    # this means we can only have one worker.

    mdlsPathPostfix = config.get("crashreport", "mdlsPathPostfix")
    mdlsDirPath = binaryDir + mdlsPathPostfix
    configItem = getBuildDownloadConfig(os.path.join(os.path.join(mdlsDirPath, binaryPath), "binary-config.txt"))
    if (not configItem):
        print "Falt error, the download config cannot be find in " + binaryDir
        return None
    download_buildscirpt = os.path.join(os.path.dirname(__file__), '../download_build.py')
    print download_buildscirpt
    downloadScript = "python " + download_buildscirpt + " /item:" + configItem + " /itemFilter:" + binaryPath + " downloadall"
    print downloadScript
    subprocess.call(downloadScript, shell=True)

    slashSeparateGUID = str(uuid.UUID(crashReportUUID)).upper()
    print ("mfind guid: " + slashSeparateGUID)
    retryCount = 0
    while(retryCount < 30):
        print("Wait for the mdfind works...")
        time.sleep(0.5)
        retryCount = retryCount + 1
        if (checkSpotlightFinishedIndex(slashSeparateGUID, appName, binaryPath)):
            break

    symPath = os.path.join(buildPath, appName + ".dSYM")
    if (not os.path.exists(symPath)):
        print "Try to download build failed." + binaryDir
        return None
    symScriptPath = os.path.join(os.path.dirname(__file__), 'SymbolicateReport.sh')
    subprocess.call(["sh", symScriptPath, crashReportPath, symPath, resultReportId])
    return resultReportId

if __name__ == '__main__':
    crashReport = sys.argv[1]
    path = convert(crashReport)
    print path
