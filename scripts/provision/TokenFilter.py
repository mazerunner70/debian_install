#!/usr/bin/python

import sys
for line in sys.stdin:
    if line.startswith("{\"token\": \""):
        sys.stderr.write("DEBUG: got line: " + line)
#        sys.stdout.write(line)
        newString = line[11:-3]
        sys.stdout.write(newString)