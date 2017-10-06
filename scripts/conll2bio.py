#!/usr/bin/env python

from __future__ import print_function
import sys

import FileTools

def main(args):
    if len(args) < 3:
        print("Usage:", args[0], "<if> <of>")
        return -1

    with FileTools.openReadFile(args[1]) as ifh, FileTools.openWriteFile(args[2]) as ofh:
        words = []
        tags = []
        v = None

        for l in ifh:
            e = l.rstrip().split("\t")

            if len(e) < 3:
                ofh.write(v+" "+" ".join(words)+" ||| "+" ".join(tags)+"\n")
                words = []
                tags = []
            else:
                t = e[2]
                if t == 'B-V':
                    v = str(len(words))
                elif t != 'O':
                    if t.find("ARG") != -1:
                        t = t.replace("ARG", "A")
                    else:
                        t = t.replace("-", "-AM-")

                words.append(e[1])
                tags.append(t)


        if len(words):
            ofh.write(" ".join(words) + " ||| " + " ".join(tags) + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))




