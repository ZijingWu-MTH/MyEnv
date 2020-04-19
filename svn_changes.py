import sys
import util
import os
import subprocess
import codecs
import re;
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations
#!/usr/bin/env python
import signal

def changeContains(changeLines, changeText):
    for line in changeLines:
        if (changeText in line and re.match("^(\+|-)", line)):
            return True
    return False
 
path = sys.argv[1]
text = sys.argv[2]
log_xml = subprocess.check_output(["svn", "log", "--xml", path])
dom = parseString(log_xml)

# we doesn't using binary search, which may have ABA issue.
logEntries = dom.getElementsByTagName('logentry')
for logEntry in logEntries:
    revision = logEntry.attributes['revision']
    revision = int(revision.value)
    try:
        print "check revision: " + str(revision)
        change = subprocess.check_output(["svn", "diff", "-r", str(revision) + ":" + str(revision - 1), path])
        if ("does not exist in the repository or refers to an unrelated object" in change):
            continue;
        changeLines = change.split('\n') 
        if (changeContains(changeLines, text)):
            print "--------------------------"
            print logEntry.toxml()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print "check the revision:" + str(revision)  + " failed."

     
