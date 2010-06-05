#!/usr/bin/python
# -*- coding:Utf-8 -*-

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        open("/home/psycojoker/code/python/ulr/urls", "a").write(sys.argv[1] + "\n")
    else:
        print "Need arg"
