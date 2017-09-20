#!/usr/bin/env python

from __future__ import print_function

import sys
from FileTools import *

def main(args):
    argc = len(args)

    if argc < 2:
        print("Usage:",args[0],"<if> <of>")
        return -1

    with open(args[1]) as ifh, openWriteFile(args[2]) as ofh:
        for l in ifh:
            gen_output(l, ofh)

    return 0

def gen_output(l, ofh):
    l = l.rstrip()
    # print(l)
    e = l.split(" ||| ")

    if len(e) != 2:
        print("bad line",l)
        return

    words = e[0].split(" ")
    words.pop(0)
    labels = e[1].split(" ")

    n = len(words)
    if  len(labels) != n:
        print("number of words",n,"!= number of labels",len(labels))
        return

    inArg = 0
    for i in range(n):
        if labels[i][0] == 'I':
            if inArg:
                ofh.write("\n")
            else:
                inArg = 1

            ofh.write(words[i].lower()+"\t*")
        else:
            if inArg:
                ofh.write(")\n")
                inArg = 0

            if labels[i] == 'O':
                ofh.write(words[i].lower()+"\t*\n")
            elif labels[i] == 'B-V':
                ofh.write(words[i].lower()+"\t(V*)\n")
            elif labels[i][:3] == 'B-A':
                ofh.write(words[i].lower()+"\t("+labels[i][2:]+"*")
                inArg = 1
            else:
                print("Bad label",labels[i])
                sys.exit(-1)

    if inArg:
        ofh.write(")\n")

    ofh.write("\n")


if __name__ == "__main__":
    sys.exit(main(sys.argv))


