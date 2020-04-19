import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/whoosh/src'))
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from whoosh.query import *
import util
import subprocess
import codecs

if (len(sys.argv) < 2):
    print "Please supply the query sentence, for example: Python query_service.py \"retur* AND (path:ui id:animate)\""
    sys.exit(0)

queryStr = unicode(sys.argv[1], "utf-8")
    
rootPath = os.environ.get("ROOT")
indexDir = os.path.join(rootPath, "_indexdir_")
ix = open_dir(indexDir)
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse(queryStr)
    results = searcher.search(query, limit=5000)
    for result in results:
        print result["path"]
