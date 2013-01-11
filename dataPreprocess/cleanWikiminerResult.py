#!/usr/bin/env python
#encoding=utf8

import sys
sys.path.append('../')

from stemmer.porterStemmer import PorterStemmer


if __name__ == "__main__":
    # files setting
    semwiki_file = "../cleanData/Hulth2003/words_pair.simvalue.dict"
    clean_semwiki_file = "../cleanData/Hulth2003/words_pair.wiki.clean.dict"

    # stemmer
    stemmer = PorterStemmer()

    raw_numitems = 0
    new_numitems = 0
    tri_dict = {}
    for line in open(semwiki_file):
        raw_numitems += 1
        triparts = line.strip('\n').split(' ')

        # to lower case
        triparts[0] = triparts[0].lower()
        triparts[1] = triparts[1].lower()
        # stemming
        triparts[0] = stemmer.stem(triparts[0], 0, len(triparts[0])-1)
        triparts[1] = stemmer.stem(triparts[1], 0, len(triparts[1])-1)

        synth_key = triparts[0] + '_' + triparts[1]
        if synth_key not in tri_dict:
            tri_dict[synth_key] = triparts[2]
            new_numitems += 1

    wfd = open(clean_semwiki_file, 'w')
    for key in tri_dict.keys():
        triparts = key.split('_')
        triparts.append(tri_dict[key])
        wfd.write("%s %s %s\n" % (triparts[0], triparts[1], triparts[2]))
    wfd.close()

    print "Raw number of items: %d. After cleaning, number of items: %d.\n"\
            % (raw_numitems, new_numitems)
