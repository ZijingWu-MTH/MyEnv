import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/whoosh/src'))
from whoosh.index import create_in
from whoosh.fields import *
import util
import subprocess
import codecs


schema = Schema(path=ID(stored=True), content=TEXT)
rootPath = os.environ.get("ROOT")
indexDir = os.path.join(rootPath, "_indexdir_")
if (os.path.exists(indexDir)):
    util.removeFolder(indexDir)
os.mkdir(indexDir)
ix = create_in(indexDir, schema)
writer = ix.writer()

fileListfilePath = os.path.join(rootPath, "filelist.filtered")
platformName = util.getPlatformName()
filePaths = open(fileListfilePath).readlines()
handledFileCount = 0
for filePath in filePaths:
    handledFileCount = handledFileCount + 1
    if (handledFileCount % 100 == 0):
        print "The progress: %d handled in %d" % (handledFileCount, len(filePaths))
        
    try:
        #print "handle %s" % (filePath)
        filePath = filePath.strip()
        if (not os.path.isfile(filePath)):
            continue
        infile = codecs.open(filePath, encoding='utf-8')
        content = infile.read()
        infile.close()
        writer.add_document(path= unicode(filePath), content= content)
        infile.close()
    except Exception, e:
        print "skip %s because of error %s happen" % (filePath, e)
writer.commit()
print "finished commit"
#def index_my_docs(dirname, clean=False):
#  if clean:
#    clean_index(dirname)
#  else:
#    incremental_index(dirname)


#def incremental_index(dirname)
#    ix = index.open_dir(dirname)

#    # The set of all paths in the index
#    indexed_paths = set()
#    # The set of all paths we need to re-index
#    to_index = set()

#    with ix.searcher() as searcher:
#      writer = ix.writer()

#      # Loop over the stored fields in the index
#      for fields in searcher.all_stored_fields():
#        indexed_path = fields['path']
#        indexed_paths.add(indexed_path)

#        if not os.path.exists(indexed_path):
#          # This file was deleted since it was indexed
#          writer.delete_by_term('path', indexed_path)

#        else:
#          # Check if this file was changed since it
#          # was indexed
#          indexed_time = fields['time']
#          mtime = os.path.getmtime(indexed_path)
#          if mtime > indexed_time:
#            # The file has changed, delete it and add it to the list of
#            # files to reindex
#            writer.delete_by_term('path', indexed_path)
#            to_index.add(indexed_path)

#      # Loop over the files in the filesystem
#      # Assume we have a function that gathers the filenames of the
#      # documents to be indexed
#      for path in my_docs():
#        if path in to_index or path not in indexed_paths:
#          # This is either a file that's changed, or a new file
#          # that wasn't indexed before. So index it!
#          add_doc(writer, path)

#      writer.commit()
