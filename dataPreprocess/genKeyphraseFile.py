#!/usr/bin/env python
#encoding=utf8

# This script extract the keyphrase from raw labeled
# file and output them in new files with one phrase
# per-line.
# What's more, we should filter keyphrases those don't
# occur in 'abstr' files.
#
# Anthor : anthonylife
# Date   : 1/13/2013

import os

dockeysuffix  = "uncontr"
outputsuffix  = "keyword"
doctextsuffix = "abstr"

def substr(candi_file):
    if candi_file.find(dockeysuffix) != -1:
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
    in_keyphrase_num = 0
    out_keyphrase_num = 0
    for i, type_docs in enumerate(doclist):
        for doc in type_docs:
            inputfile = dir_output_file[i]\
                    +doc.split('/')[-1].split('.')[0]\
                    +"."+doctextsuffix
            outputfile = dir_output_file[i]\
                    +doc.split('/')[-1].split('.')[0]\
                    +"."+outputsuffix

            # read normal text (title and abstract)
            docwordlist= []
            for line in open(inputfile):
                line = line.strip('\r\n ')
                wordssegment = line.split(' ')
                for word in wordssegment:
                    docwordlist.append(word.split('_')[0].lower().strip(' '))
            wholedoctext = ' '.join(docwordlist)
            #print inputfile
            #print wholedoctext

            wfd = open(outputfile, 'w')
            linelist = []
            for line in open(doc):
                line = line.strip('\t\r\n')
                linelist.append(line)
            keyphrasestext = " ".join(linelist)
            keyphrasestext = keyphrasestext.lower()
            textunits = keyphrasestext.split("; ")
            #print textunits
            for textunit in textunits:
                if wholedoctext.find(textunit)!=-1:
                    #print textunit
                    wfd.write("%s\n" % textunit)
                    in_keyphrase_num += 1
                else:
                    out_keyphrase_num += 1
            wfd.close()
            #raw_input()
    print 'in_keyphrase_num: %d' % in_keyphrase_num
    print 'out_keyphrase_num: %d' % out_keyphrase_num
