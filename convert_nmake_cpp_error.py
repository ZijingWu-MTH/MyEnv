import util
import sys
import re

logLines = util.getLinesWithoutLineEnd(sys.argv[1])

result = []
#d:\call\call.h(4) : fatal error C1083: Cannot open include file: 'xxx.h': No such file or directory
pattern = re.compile("^\s*([^()]+)\((\d+)\) : ((fatal )?error C\d+:.*)$")
for line in logLines:
    regMatch = pattern.match(line)
    if (regMatch):
       filePath = regMatch.group(1);
       lineNum = regMatch.group(2);
       colNum = regMatch.group(3);
       msg = regMatch.group(4);
       #print $file . ":" . $lineNum . ":" . $msg. " " . $projName . "--\n";
       newLine = "%s:%s:%s:%s" % (filePath, lineNum, colNum, msg);
       result = result + [newLine]

outputFile = open(sys.argv[2], 'w')
outputFile.write("\n".join(result))
outputFile.close()
