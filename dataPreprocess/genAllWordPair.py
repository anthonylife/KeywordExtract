#!/usr/bin/env python
#encoding=utf8

# Task:In order to calculate the similarity between words by
# WikipediaMiner, we need to get all candidate pairs in the
# corpus to be used. Currently, we want to store all the pairs
# in the disk and also can return the pair hash list.
#
# Author: anthonylife
# Date:   1/8/2013

import os

class GenCorpusWordPair:
    ''' The class used to generate all word pairs in the
        specificed corpus
    '''
    def __init__(self, srcrootdir, tarrootdir, docsuffix=None):
        self.srcrootdir = srcrootdir
        self.tarrootdir = tarrootdir
        self.docsuffix = docsuffix
        self.words_pair = set([])
        self.doclist = []

    def getdoclist(self):
        for rootdir in self.srcrootdir:
            candi_files = os.listdir(rootdir)
            # filter file by suffix if existed
            if self.docsuffix:
                candi_files = filter(self.substr, candi_files)
            candi_files = map(lambda x: rootdir+x, candi_files)
            self.doclist = self.doclist + candi_files

    def genAllPair(self):
        for doc in self.doclist:
            self.readpairs(doc)

    # read data from document and add unique pair into dic
    def readpairs(self, doc):
        doc_words = set([])
        print doc
        for line in open(doc):
            res = line.strip('\n').split(' ')
            for word in res:
                if word not in doc_words:
                    for src_word in doc_words:
                        word_pair = src_word+'_'+word if src_word < word \
                                else word+'_'+src_word
                        if word_pair not in self.words_pair:
                            self.words_pair.add(word_pair)
                    doc_words.add(word)

    def output(self, output_file):
        wfd = open(output_file, 'w')
        self.words_pair = sorted(self.words_pair, reverse=False)
        for word_pair in self.words_pair:
            res = word_pair.split('_')
            wfd.write("%s %s\n" % (res[0], res[1]))
        wfd.close()

    def substr(self, candi_file):
        if candi_file.find(self.docsuffix) != -1:
            return True
        return False


def main():
#==========
    # variables setting
    srcdir = ["../../data/sourcedata/Hulth2003/Train/",\
            "../../data/sourcedata/Hulth2003/Test/", \
            "../../data/sourcedata/Hulth2003/Validation/"]
    file_suf = "abstr"
    outputfile = "../cleanData/Hulth2003/words_pair.dict"

    # instance of class
    pair_gentor = GenCorpusWordPair(srcdir, None, file_suf)

    # get doc list in the complete corpus
    pair_gentor.getdoclist()

    # generate all pairs
    pair_gentor.genAllPair()

    # output all pairs
    pair_gentor.output(outputfile)


def test():
#==========
    # variables setting
    srcdir = ["../unitTest/genAllWordPair/"]
    file_suf = "txt"
    outputfile = "../unitTest/genAllWordPair/result"

    # instance of class
    pair_gentor = GenCorpusWordPair(srcdir, None, file_suf)

    # get doc list in the complete corpus
    pair_gentor.getdoclist()

    # generate all pairs
    pair_gentor.genAllPair()

    # output all pairs
    pair_gentor.output(outputfile)

if __name__ == "__main__":
    #main()
    test()
