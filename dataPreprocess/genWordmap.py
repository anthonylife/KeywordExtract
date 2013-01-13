#!/usr/bin/env python
#encoding=utf8

import os, re, sys
sys.path.append('../')

from globalSetting import POS, REG_EXP
from stemmer.porterStemmer import PorterStemmer

class WordmapGenerator:
    '''This class generates word map for the specified
       corpus. Because of the task for keyphrase extraction,
       we need to specify the POS sets of which the words
       will be saved.
       It also needs to be general so that all keyphrase
       extraction methods can utilize it.
       As we will use pos tags, we construct word map from
       cleaned text.
       Note that some keyphrases are not existed in the abstract,
       so we need to index them in dictionary.
    '''
    def __init__(self, dir_text_file, output_wordmap_file, \
            pos_sets, reg_exp, docsuffix, kpdocsuffix):
        self.dir_text_file = dir_text_file
        self.output_wordmap_file = output_wordmap_file
        self.pos_sets = pos_sets
        self.docsuffix = docsuffix
        self.kpdocsuffix = kpdocsuffix

        self.stemmer = PorterStemmer()
        self.dict_words = []
        self.pattern = re.compile(reg_exp)
        self.doclist = []
        self.doclist = self.getdoclist(1)

    def getdoclist(self, choice):
        temp_doclist = []
        for rootdir in self.dir_text_file:
            candi_files = os.listdir(rootdir)
            # filter file by suffix if existed
            if choice == 1:
                candi_files = filter(self.doc_substr, candi_files)
            elif choice == 2:
                candi_files = filter(self.kpdoc_substr, candi_files)
            candi_files = map(lambda x: rootdir+x, candi_files)
            temp_doclist = temp_doclist + candi_files
        return temp_doclist

    def doc_substr(self, candi_file):
        if candi_file.find(self.docsuffix) != -1:
            return True
        return False

    def kpdoc_substr(self, candi_file):
        if candi_file.find(self.kpdocsuffix) != -1:
            return True
        return False

    def genwordmap(self):
        temp_words = set([])
        for doc in self.doclist:
            for line in open(doc):
                words = line.strip("\n\r ").split(' ')
                for word in words:
                    biparts = word.split('_')
                    # words processing
                    # ================
                    biparts[0] = biparts[0].lower()
                    biparts[0] = self.stemmer.stem(biparts[0], 0,\
                            len(biparts[0])-1)
                    if len(biparts) == 2 and biparts[1] in self.pos_sets\
                            and self.pattern.match(biparts[0]):
                        temp_words.add(biparts[0])
                    # ================
        self.doclist = self.getdoclist(2)
        temp_keywords = set([])
        miss_keywords = 0
        for doc in self.doclist:
            for line in open(doc):
                textunits = line.strip('\n\r ').split(" ")
                for textunit in textunits:
                    # words processing
                    # ================
                    textunit = textunit.lower()
                    textunit = self.stemmer.stem(textunit, 0, len(textunit)-1)
                    # ================
                    temp_keywords.add(textunit)
                    if not textunit in temp_words:
                        temp_words.add(textunit)
                        miss_keywords += 1
        self.dict_words = sorted(temp_words)
        print "Number of unique keywords: %d, " % len(temp_keywords)
        print "number of left missing words: %d.\n" % miss_keywords

    def output_wordmap(self):
        wfd = open(self.output_wordmap_file, 'w')
        for i,word in enumerate(self.dict_words):
            wfd.write("%s %d\n" % (word, i+1))
        wfd.close()


def main():
    # files path setting
    dir_text_file = ["../cleanData/Hulth2003/Test/", \
                    "../cleanData/Hulth2003/Train/", \
                    "../cleanData/Hulth2003/Validation/"]
    output_wordmap_file = "../cleanData/Hulth2003/words_map.clean.dict"
    pos_sets = POS
    reg_exp = REG_EXP
    docsuffix = "abstr"
    kpdocsuffix = "keyword"

    # wordmap generation
    wordmapGenerator = WordmapGenerator(dir_text_file,\
            output_wordmap_file, pos_sets, reg_exp,\
            docsuffix, kpdocsuffix)
    wordmapGenerator.genwordmap()
    wordmapGenerator.output_wordmap()

def test():
    # files path setting
    dir_text_file = ["../unitTest/dataPreprocess/genWordmap/"]
    output_wordmap_file = "../unitTest/dataPreprocess/genWordmap/word.txt"
    pos_sets = POS
    reg_exp = REG_EXP
    docsuffix = "abstr"
    kpdocsuffix = "keyword"

    # wordmap generation
    wordmapGenerator = WordmapGenerator(dir_text_file,\
            output_wordmap_file, pos_sets, reg_exp,\
            docsuffix, kpdocsuffix)
    wordmapGenerator.genwordmap()
    wordmapGenerator.output_wordmap()

if __name__ == "__main__":
    main()
    #test()
