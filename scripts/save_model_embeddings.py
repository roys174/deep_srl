#!/usr/bin/env python

import sys
import numpy as np

def main(args):
    if len(args) < 2:
        print("Usage:",args[0],"<work dir>")
        return -1

    work_dir = args[1]

    model = np.load(work_dir+'/model.npz')
    embeddings = model['embedding_0']

    with open(work_dir+'/word_dict') as ifh:
        word_list = ifh.readlines()

    with open(work_dir+'/output_embeddings.dat', 'w') as ofh:
        ofh.write(str(len(embeddings))+" "+str(len(embeddings[0]))+'\n')
        for i in range(len(word_list)):
            ofh.write(word_list[i].rstrip() + " ")
            ofh.write(" ".join([str(x) for x in embeddings[i]]) + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
