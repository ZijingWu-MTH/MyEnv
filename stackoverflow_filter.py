from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import httplib
import sys
import urllib
import xml.etree.cElementTree as ET

class HTMLToXML(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.stack = [] 
        self.currentNode = None

    def getRoot(self):
        return self.stack[0]
    
    def handle_starttag(self, tag, attrs):
        self.currentNode = ET.Element(tag)
        if (len(self.stack) > 0):
            parentNode = self.stack.pop()
            parentNode.append(self.currentNode)
            self.stack.append(parentNode)
        self.stack.append(self.currentNode)
        self.currentNode.attrib = dict(attrs)
            
    def handle_endtag(self, tag):
        self.currentNode = self.stack.pop()

    def handle_data(self, data):
        # for html head
        if (self.currentNode != None):
            self.currentNode.text = data

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        #c = unichr(name2codepoint[name])
        c = ""
    def handle_charref(self, name):
        if name.startswith('x'):
            #c = unichr(int(name[1:], 16))
            c = ""
        else:
            c = ""
            #c = unichr(int(name))
    def handle_decl(self, data):
        pass

def FilterOnePage(pageNum):
    params = urllib.urlencode({
        'page': pageNum,
        'pagesize': 50,
        'sort': 'newest',
    })
    if (siteName == "SO"):
        siteHost = "stackoverflow.com"
        url = "/questions/tagged/c%2b%2b?" + params
    else:
        siteHost = "ux.stackexchange.com"
        url = "/questions?" + params
    conn = httplib.HTTPConnection(siteHost)
    conn.request("GET", url) 
    r1 = conn.getresponse()
    data1 = r1.read()
    conn.close()
    parser = HTMLToXML()
    parser.feed(data1)

    result = []
    questions = parser.getRoot().findall(".//div[@class='question-summary']")
    for question in questions:
        voteElment = question.find(".//span[@class='vote-count-post ']/strong")
        hyperLinkElement = question.find(".//a[@class='question-hyperlink']")
        userReputationElement = question.find(".//span[@class='reputation-score']")
        if (voteElment == None or userReputationElement == None or hyperLinkElement == None):
            continue

        reputationStr = "0"
        if (not userReputationElement.text.strip() == ""):
            reputationStr = userReputationElement.text.replace(",", "")

        voteCount = int(voteElment.text)
        if (voteCount < voteMin and ( voteCount < 2 or reputationStr.find("k") <= 0 and int(reputationStr) < reputationMin)):
            continue
        result = result + [("http://" + siteHost + hyperLinkElement.attrib["href"], voteCount, reputationStr)]
    return result;

siteName = "SO" 
if (len(sys.argv) > 1):
    siteName = sys.argv[1]

voteMin = 4
if (siteName == "UX"):
    voteMin = 3 
if (len(sys.argv) > 2):
    voteMin = int(sys.argv[2])

pageNum = 4
if (siteName == "UX"):
    pageNum = 2

if (len(sys.argv) > 3):
    pageNum = int(sys.argv[3])

reputationMin = 1000 
if (siteName == "UX"):
    reputationMin = 500
if (len(sys.argv) > 4):
    reputationMin = int(sys.argv[4])

results = []
for index in range(0, pageNum):
    results = results + FilterOnePage(index)
        
for (url, voteNum, userReputation) in results:
    print "Vote Count:" + str(voteNum) + " User Reputation:" + userReputation
    print "</br>"
    print "<a href='%s'>%s</a>" % (url, url)
    print "</br>"

