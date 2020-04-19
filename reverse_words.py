import sys
import os
import collections
import re

reg = " +"
if (len(sys.argv) > 0):
    reg = sys.argv[1]

for line in sys.stdin:
    line = line.strip()
    words = re.split(reg, line)
    words = words[::-1]
    result = []
    for word in words:
        if (len(word) == 0):
            continue
        result = result + [word]
    print result

