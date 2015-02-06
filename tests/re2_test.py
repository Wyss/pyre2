#!/usr/bin/env python
import os
import sys
import glob
import doctest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# os.chdir(os.path.dirname(__file__) or '.')

def testall():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    # print(path)
    searchstr = os.path.join(path,'re2_testfiles', "*.txt")
    # print(searchstr)
    files = glob.glob(searchstr)
    # print(files)
    for fn in files:
        print("Testing %s..." % fn)
        doctest.testfile(fn, module_relative=False)

if __name__ == "__main__":
    testall()
