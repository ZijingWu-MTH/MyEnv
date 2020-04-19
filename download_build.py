import os
import os.path
import re
import subprocess
import sys
import traceback
import urllib2
import urlparse
import xml.etree.cElementTree as ET

def handleVariableString(variables, str):
    for k, v in variables.items():
        str = str.replace("$" + k, v)
    return str

copyToWork = False
downloadAll = False
forceRefresh = False
verbose = False
itemName = "daily"
itemFilter = None

index = 0
while (index < len(sys.argv)):
    if (sys.argv[index] == "downloadall"):
        downloadAll = True;
    if (sys.argv[index] == "force"):
        forceRefresh = True;
    if (sys.argv[index] == "verbose"):
        verbose = True;
    if (sys.argv[index].startswith("/item:")):
        itemName = sys.argv[index].replace("/item:", "")
    if (sys.argv[index].startswith("/itemFilter:")):
        itemFilter = sys.argv[index].replace("/itemFilter:", "")
        print "itemFilter = " + itemFilter

        
    index = index + 1


configPath = os.path.join(os.path.dirname(__file__), 'download_build.config')
xmldoc = ET.parse(configPath).getroot()
configNode = xmldoc.find((".//download_config_item[@name='%s']" % itemName))
pageUrlNode = configNode.find(".//pageUrl") 
rootUrl = pageUrlNode.text
maxNum = int(configNode.get("maxNum"))
urlParseResult = urlparse.urlparse(rootUrl)

print rootUrl
response = urllib2.urlopen(rootUrl)
html = response.read()
pattern = configNode.find(".//urlPattern").text

#<folderPrefix>/Users/ZijingWu/Downloads/binary/</folderPrefix>
folderPrefix = configNode.find(".//folderPrefix").text

buildItem = [m.group(1) for m in re.finditer(pattern, html)]

if (downloadAll):
    num = len(buildItem)
    if (num > maxNum):
        num = maxNum
    indexRange = range(1, num)
else:
    indexRange = range(1, 1)
    while ((indexRange < 50) and indexRange < len(buildItem)):
        item = buildItem[-1 * indexRange]
        print "%s:%s" % (indexRange, item)
        indexRange = indexRange + 1

    index = raw_input("Please select the one you want to download:")
    if (index.strip() == ""):
        indexRange = range(1, 1)
    else:
        index = range(1, int(index))

    if (index == 0):
        sys.exit()

for index in indexRange:
    buildUrl = urlparse.urlunparse((urlParseResult.scheme, urlParseResult.netloc, buildItem[-1 * index], "", "", ""));
    if (itemFilter and not re.search(itemFilter, buildUrl)):
        continue

    #<variables>
    #    <variable name="versionNum" pattern="r(\d\d\d\d)"/>
    #</variables>
    variableNodes = configNode.findall(".//variable")
    variables = {}
    for variable in variableNodes:
        name = variable.get('name')
        valuePattern = variable.get('pattern')
        m = re.search(valuePattern, buildUrl)
        if (m != None):
            valuePattern = m.group(1)
        variables[name] = valuePattern
    print variables

    try:
        #<folderNamePattern>(\d\d\d\d)</folderNamePattern>
        folderNamePattern = configNode.find(".//folderNamePattern").text
        m = re.search(folderNamePattern, buildUrl)
        if (m == None):
            raise Exception("The folder name pattern doesn't match the URL.")
        targetDirPath = os.path.join(folderPrefix, m.group(0))
        if (not os.path.exists(targetDirPath)):
            os.makedirs(targetDirPath)
        os.chdir(targetDirPath)
        fileNames = []
        fileGroup = configNode.find(".//files") 
        files = fileGroup.findall("./file")
        #<file url="m500Internal/m500Internal.dSYM.zip" destPath="m500Internal.dSYM.zip" scriptTemplate=""/>
        for file in files:
            url = handleVariableString(variables, file.get('url'))
            destPath = handleVariableString(variables, file.get('destPath'))
            scriptTemplate = handleVariableString(variables, file.get('scriptTemplate'))
            fileNames = fileNames + [(url, destPath, scriptTemplate)]
        
        for (fileName, destPath, scriptTemplate) in fileNames:
            buildUrlParseResult = urlparse.urlparse(buildUrl)
            fileUrl = urlparse.urlunparse((buildUrlParseResult.scheme, buildUrlParseResult.netloc, os.path.join(buildUrlParseResult.path, fileName), "", "", ""));
            print fileUrl
            outputFilePath = os.path.join(targetDirPath, destPath)
            if ((os.path.isfile(outputFilePath+".done") or os.path.isfile(outputFilePath)) and not forceRefresh):
                print "Skip... because it exist already."
                continue
            
            gzFile = urllib2.urlopen(fileUrl) 
            output = open(outputFilePath, 'wb') 
            output.write(gzFile.read()) 
            output.close() 
            script = scriptTemplate.replace("$_", outputFilePath)
            print "Current dir: " + os.getcwd()
            print script
            subprocess.check_output(script, shell=True)
            f = open(outputFilePath + ".done", "w")
            f.write("done")
            f.close()
            if os.path.isfile(outputFilePath):
                os.unlink(outputFilePath)

        scriptTemplate = configNode.find(".//itemPostScript").text
        script = scriptTemplate.replace("$_", targetDirPath) 
        print "Current dir: " + os.getcwd()
        print script
        subprocess.check_output(script, shell=True)
    except KeyboardInterrupt:
        raise
    except:
        print "Error happen try to downloads or handle the result file:" + buildUrl
        traceback.print_exc()
        pass

os.chdir(folderPrefix)
script = xmldoc.find(".//postScript").text
subprocess.check_output(script, shell=True)



