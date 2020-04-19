import os
import sys
import math
import util
from optparse import OptionParser
import base64
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
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/slowaes/python'))
import aes

if __name__ == "__main__":
    print" usage: python encrypt.py -f filePath -d True"
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filePath", help="provide the file for encrypt.")
    parser.add_option("-d", "--decrypt", dest="decrypt", help="provide the file for decrypt.")
    
    (options, args) = parser.parse_args()
    if (not options.filePath):
        print "Please provide the file for encrypt or decrypt."
        sys.exit(0)



    path = options.filePath;
    content = util.readSmallFileAsString(path)

    userInputStr = raw_input("Please input the password:")
    userInputStr = userInputStr + (" " * (16 - len(userInputStr)));

    if (path and os.path.exists(path) and os.path.isfile(path)):
        newFileName = path + "." + util.id_generator(6);
        print "backup the file to :" + newFileName
        shutil.copyfile(path, newFileName)

    moo = aes.AESModeOfOperation()
    if (not (options.decrypt.lower() == "true")):
        result = aes.encryptData(userInputStr, content)
    else:
        result = aes.decryptData(userInputStr, content)
    util.writeSmallFileAsString(path, result);
