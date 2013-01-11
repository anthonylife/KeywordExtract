#!/usr/bin/env python
#encoding=utf8

# This script extract the keyphrase from raw labeled
# file and output them in new files with one phrase
# per-line.

import os

docsuffix = "uncontr"
outputsuffix = "keyword"

def substr(candi_file):
    if candi_file.find(docsuffix) != -1:
        return True
    return False

if __name__ == "__main__":
    # Path setting
    dir_text_file = ["../../data/sourcedata/Hulth2003/Train/",\
                    "../../data/sourcedata/Hulth2003/Test/",\
                    "../../data/sourcedata/Hulth2003/Validation/"]
    dir_output_file = ["../cleanData/Hulth2003/Train/",\
                     "../cleanData/Hulth2003/Test/",\
                     "../cleanData/Hulth2003/Validation/"]
    # Important variable setting
    doclist = []

    # Get document list
    for rootdir in dir_text_file:
        candi_files = os.listdir(rootdir)
        # filter file by suffix if existed
        candi_files = filter(substr, candi_files)
        candi_files = map(lambda x: rootdir+x, candi_files)
        doclist.append(candi_files)

    # Parse the file and output
    for i, type_docs in enumerate(doclist):
        for doc in type_docs:
            outputfile = dir_output_file[i]\
                    +doc.split('/')[-1].split('.')[0]\
                    +"."+outputsuffix
            #print outputfile
            #raw_input()
            wfd = open(outputfile, 'w')
            linelist = []
            for line in open(doc):
                line = line.strip('\t\r\n')
                linelist.append(line)
            keyphrases_text = " ".join(linelist)
            textunits = keyphrases_text.split("; ")
            for textunit in textunits:
                wfd.write("%s\n" % textunit)
            wfd.close()
