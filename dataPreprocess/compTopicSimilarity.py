#!/usr/bin/env python
#encoding=utf8

# Task:The main class is responsible to generate edge topic features
# between word.
# Main procedures:
#   1.In order to use Gibbslda++ to calculate the topic distribution,
#     we need first to convert the documents to the format which meets
#     the Gibbslda++ requirements;
#   2.Computing topic similarity between word pairs in each document.
#     Note, we only consider adjective words and noun words, while
#     other words will not be added into semantic graph.
#
# Author: anthonylife
# Date:   1/10/2013

import re, os, sys
sys.path.append('../')

from globalSetting import REG_EXP, CMD, TOPIC_POS, Stopwords
from stemmer.porterStemmer import PorterStemmer

class GetTopicDis:
    ''' Call ldaGibbs++, the opensource software, to get the topic
        distribution for words and documents. Before calling, we
        should first convert the file to the format which meets
        the requirements.
    '''
    def __init__(self, src_corp_dir, lda_doc, docsuffix):
        self.src_corp_dir = src_corp_dir
        self.lda_doc = lda_doc
        self.docsuffix = docsuffix
        self.stopWords = Stopwords()
        self.stemmer = PorterStemmer()
        self.pattern = re.compile(REG_EXP)

        self.doclist = []
        self.getdoclist()
        self.genmodel_inputfile()

    def getdoclist(self):
        for subdir in self.src_corp_dir:
            candi_files = os.listdir(subdir)
            # filter file by suffix if existed
            if self.docsuffix:
                candi_files = filter(self.substr, candi_files)
            candi_files = map(lambda x: subdir+x, candi_files)
            self.doclist = self.doclist + candi_files

    # generate the file meeting the requirements of the ldaGibbs++
    def genmodel_inputfile(self):
        wfd = open(self.lda_doc, "w")
        wfd.write("%d\n" % len(self.doclist))
        for doc in self.doclist:
            docwordlist = []
            for line in open(doc):
                line = line.strip("\n")
                docwordlist = docwordlist + self.filterwords(line)
            docwordlist = sorted(docwordlist, reverse=False)
            wfd.write("%s\n" % " ".join(docwordlist))
        wfd.close()

    # call Gibbs LDA
    def call_lda(self, topicnum, maxiter):
        # lda model parameter setting
        alpha = 1.0*topicnum / 50
        cmd = CMD + "-alpha " + str(alpha) + " -ntopics " + \
                str(topicnum) + " -niters " + str(maxiter) + \
                " -dfile " + self.lda_doc
        print "Calling Gibbs LDA"
        #os.popen(cmd)
        os.system(cmd)
        print "Finishing calling"

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
            if len(biparts) == 2 and biparts[1] in TOPIC_POS:
                if not self.stopWords.is_stopword(biparts[0])\
                        and self.pattern.match(biparts[0]):
                    save_words.append(biparts[0])
            # ============================================
        return save_words

    def substr(self, candi_file):
        if candi_file.find(self.docsuffix) != -1:
            return True
        return False


class CompTopicSimilarity:
    '''Getting the similarity between the pair of words
       based on the their topic distribution. More specifically,
       I adopt Jensen-Shannon divergence to measure their
       similarity.
    '''
    def __init__(self):
        pass

    def output_topic_dist(self):
        pass

    def comp_similarity(self, inputfile):
        pass


def generatetopic():
    # files' path setting
    src_corp_dir = ["../cleanData/Hulth2003/Train/",\
            "../cleanData/Hulth2003/Test/", \
            "../cleanData/Hulth2003/Validation/"]
    docsuffix = "abstr"
    lda_doc = "../cleanData/Hulth2003/docs.lda"

    # LDA model's parameters setting
    topicnum = 25
    maxiter = 2000

    # instance of class
    topicDisGentor = GetTopicDis(src_corp_dir, lda_doc, docsuffix)
    topicDisGentor.call_lda(topicnum, maxiter)

def computesimilarity():
    pass


def main():
    # generate topic distribution based on LDA Gibbs Sampling.
    generatetopic()

    # compute topic similarity
    computesimilarity()

if __name__ == "__main__":
    main()
