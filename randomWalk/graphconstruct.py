#!/usr/bin/env python
#encoding=utf8

# author: anthonylife
# date: 1/12/2013

import numpy as np
import re, os, sys
sys.path.append('../')

from dataPreprocess.globalSetting import REG_EXP, POS, Stopwords
from stemmer.porterStemmer import PorterStemmer

class GraphGenerator:
    '''This class mainly construct graph for basic random
       walk method.
       Method: graph construction based on sliding window
               strategy.
       Ouput : two files-->1.graph file for each document;
                           2.word id in document to word map dictionary.
       Currently, we implements two graph representation, i.e., dense
       graph representation and sprase graph representation.
    '''
    def __init__(self, dir_text_file, dir_output_file,\
            windowsize, docsuffix, wordmap_file):
        self.mapfile_suffix = ".idmap"
        self.graphfile_suffix = ".graph"
        self.stopWords = Stopwords()
        self.stemmer = PorterStemmer()
        self.pattern = re.compile(REG_EXP)

        self.dir_text_file = dir_text_file
        self.dir_output_file = dir_output_file
        self.windowsize = windowsize
        self.docsuffix = docsuffix
        self.wordmap_file = wordmap_file

        self.doclist = []
        self.getdoclist()
        self.corp_wordmap = {}
        self.readwordmap()

    def getdoclist(self):
        for rootdir in self.dir_text_file:
            candi_files = os.listdir(rootdir)
            # filter file by suffix if existed
            if self.docsuffix:
                candi_files = filter(self.substr, candi_files)
            candi_files = map(lambda x: rootdir+x, candi_files)
            self.doclist = self.doclist + candi_files

    def substr(self, candi_file):
        if candi_file.find(self.docsuffix) != -1:
            return True
        return False

    def readwordmap(self):
        for line in open(self.wordmap_file):
            biparts = line.strip("\r\n").split(" ")
            self.corp_wordmap[biparts[0]] = int(biparts[1])

    # filter words based on stopwords list and character rule
    def filterwords(self, textline):
        save_words = []
        words = textline.split(" ")
        for word in words:
            if word == " ":
                continue
            biparts = word.split("_")
            # words processing (stopword, stemming, lower)
            # ============================================
            biparts[0] = biparts[0].lower()
            biparts[0] = self.stemmer.stem(biparts[0], 0, \
                    len(biparts[0])-1)
            if len(biparts) == 2 and biparts[1] in POS:
                if not self.stopWords.is_stopword(biparts[0])\
                        and self.pattern.match(biparts[0]):
                    save_words.append(biparts[0])
            # ============================================
        return save_words

    # graph construction
    # strategy: 1.filter words accroding to POS tags;
    #           2.construct graph based on sliding window.
    def construct(self):
        for doc in self.doclist:
            doc_prefix = doc.split('/')[-1].split('.')[0]
            output_graphfile = self.dir_output_file + doc_prefix \
                    + self.graphfile_suffix
            output_mapfile = self.dir_output_file + doc_prefix \
                    + self.mapfile_suffix

            cleaned_wordslist = []
            for line in open(doc):
                line = line.strip('\n')
                cleaned_wordslist = cleaned_wordslist + self.filterwords(line)
            wordsmap_indoc = self.numword_indoc(cleaned_wordslist)
            #print wordsmap_indoc
            pairids = self.mapwordspair(wordsmap_indoc)
            pairids = sorted(pairids, key=lambda x: x[0])
            dense_graph = self.slidingwindow(cleaned_wordslist, wordsmap_indoc)
            self.output_graph('dense', dense_graph, output_graphfile)
            self.output_graph('sparse', dense_graph, output_graphfile)
            self.output_map(pairids, output_mapfile)

    def mapwordspair(self, ids_indoc):
        pairids = []
        for key in ids_indoc.keys():
            pairids.append([ids_indoc[key], self.corp_wordmap[key]])
        return pairids

    def slidingwindow(self, cleaned_wordslist, wordsmap_indoc):
        dense_graph = np.array([0.0 for i in range(len(wordsmap_indoc)\
                *len(wordsmap_indoc))])
        dense_graph = dense_graph.reshape(len(wordsmap_indoc), len(wordsmap_indoc))

        for i, word in enumerate(cleaned_wordslist):
            sliding_text = cleaned_wordslist[max(0, i-self.windowsize/2):\
                     min(len(cleaned_wordslist), i+self.windowsize/2+1)]
            for j in range(len(sliding_text)):
                if cleaned_wordslist[i] == sliding_text[j]:
                    continue
                #print cleaned_wordslist[i]
                #print sliding_text[j]
                #raw_input()
                dense_graph[wordsmap_indoc[cleaned_wordslist[i]]-1,\
                        wordsmap_indoc[sliding_text[j]]-1] += 1
        return dense_graph

    def numword_indoc(self, wordslist_indoc):
        wordsmap_indoc = {}
        word_id = 1
        for word in wordslist_indoc:
            if word not in wordsmap_indoc:
                wordsmap_indoc[word] = word_id
                word_id += 1
        return wordsmap_indoc

    def output_graph(self, choice, graphdata, graphfile):
        #print graphfile
        if choice == "dense":
            wfd = open(graphfile+'.dense', 'w')
            for i in range(len(graphdata)):
                wfd.write("%s\n"%' '.join(map(lambda x: str(x), graphdata[i])))
        elif choice == "sparse":
            wfd = open(graphfile+'.sparse', 'w')
            for i in range(len(graphdata)):
                for j in range(len(graphdata)):
                    if graphdata[i,j] != 0:
                        wfd.write("%d %d %d\n" % (i, j, graphdata[i, j]))
        wfd.close()

    def output_map(self, mapdata, mapfile):
        #print mapfile
        wfd = open(mapfile, 'w')
        for i in range(len(mapdata)):
            wfd.write("%d\n" % mapdata[i][1])
        wfd.close()

def main():
    dir_text_file = ["../cleanData/Hulth2003/Test/"]
    dir_output_file = "../features/randomWalk/"
    windowsize = 2
    docsuffix = "abstr"
    wordmap_file = "../cleanData/Hulth2003/words_map.clean.dict"

    graphGenerator = GraphGenerator(dir_text_file, dir_output_file,\
            windowsize, docsuffix, wordmap_file)
    graphGenerator.construct()

def test():
    dir_text_file = ["../unitTest/randomWalk/"]
    dir_output_file = "../unitTest/randomWalk/"
    windowsize = 2
    docsuffix = "abstr"
    wordmap_file = "../cleanData/Hulth2003/words_map.clean.dict"

    graphGenerator = GraphGenerator(dir_text_file, dir_output_file,\
            windowsize, docsuffix, wordmap_file)
    graphGenerator.construct()

if __name__ == "__main__":
    #test()
    main()
