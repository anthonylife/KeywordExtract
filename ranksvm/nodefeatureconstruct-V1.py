#!/usr/bin/env python
#encoding=utf8

'''
General idea: different from the old version, which is special for re-
implementation of Knulth's similar supervised method with the same
features, we want to provide a more flexible feature generation class.

@author: anthonylife
@date:   1/20/2013
'''
#import numpy as np
import sys, os, math
sys.path.append('../')

from dataPreprocess.filterWords import WordFilter
from dataPreprocess.globalSetting import POS, TOPIC_POS
from stemmer.porterStemmer import PorterStemmer

class NodeFeatureGenerator():
    '''This class provides a framework which is easy for feature addition
       and deletion. The following features are common features that have
       been used in keywords/keyphrase extraction task.

       Features: the first three features listed below must be generated.
       1.TF;
       2.DF;
       3.POSITION;
       4.TF-IDF;
       5.lenText;
       6.POS-Tagging;

       Note: all features should be normalized to 0-1.
    '''
    def __init__(self, posset, feature_bittag, dir_text, text_suffix,\
            dir_feature, feature_suffix, dir_manualkp, manualkp_suffix,\
            wordsmap_file, featurenum, nonposfeature):
        # receving input
        self.posset          = posset
        self.feature_bittag  = feature_bittag
        self.dir_text        = dir_text
        self.text_suffix     = text_suffix
        self.dir_feature     = dir_feature
        self.feature_suffix  = feature_suffix
        self.dir_manualkp    = dir_manualkp
        self.manualkp_suffix = manualkp_suffix
        self.wordsmap_file   = wordsmap_file
        self.featurenum      = featurenum
        self.nonposfeature   = nonposfeature

        # inner variable setting
        self.poslist        = list(posset)
        self.featuretype    = sum(feature_bittag)
        self.stemmer        = PorterStemmer()
        self.wordsmap       = self.loadmap()
        self.wordfilter     = WordFilter()
        self.doctext, self.doctags, self.worddf = self.loaddoctext()
        self.manualkeywords = self.getmanualkeywords()


    def generatefeature(self, norm_method):
        # running
        self.corpfeature    = self.mkfeatures()
        self.normalization(norm_method)
        self.outputdocfeatures()

    def loadmap(self):
        wordsmap = {}
        for line in open(self.wordsmap_file):
            biparts = line.strip('\n').split(' ')
            wordsmap[biparts[0]] = biparts[1]
        return wordsmap

    def loaddoctext(self):
        doctext = {}; doctags = {}; worddf = {}
        doclist = self.getdoclist(self.substr_text, self.dir_text)
        for doc in doclist:
            docwordlist = []; doctaglist = []
            for line in open(doc):
                clean_words, tags = self.wordfilter.filterwords\
                        (line.strip('\r\n '))
                docwordlist += clean_words
                doctaglist  += tags
            doctext[doc] = docwordlist
            doctags[doc] = doctaglist

            # compute document frequency for words
            for word in set(docwordlist):
                if word in self.wordsmap:
                    wordid = self.wordsmap[word]
                    if wordid in worddf:
                        worddf[wordid] += 1
                    else:
                        worddf[wordid] = 1
        return doctext, doctags, worddf

    def getdoclist(self, substr_func, dir_file):
        doclist = []
        for subdir in dir_file:
            candi_files = os.listdir(subdir)
            # filter file by suffix if existed
            candi_files = filter(substr_func, candi_files)
            candi_files = map(lambda x: subdir+x, candi_files)
            doclist = doclist + candi_files
        return doclist

    def substr_text(self, candi_file):
        if candi_file.find(self.text_suffix) != -1:
            return True
        return False

    def substr_manualkp(self, candi_file):
        if candi_file.find(self.manualkp_suffix) != -1:
            return True
        return False

    def getmanualkeywords(self):
        '''segment each keyphrase into keywords
        '''
        manualkeywords = {}
        doclist = self.getdoclist(self.substr_manualkp,\
                self.dir_manualkp)
        for doc in doclist:
            docname = doc.split('/')[-1].split('.')[0]
            keywordset = set([])
            for line in open(doc):
                for word in line.strip('\r\n ').split(' '):
                    word = word.lower()
                    word = self.stemmer.stem(word, 0, \
                        len(word)-1)
                    if word not in keywordset:
                        keywordset.add(word)
            keywordset = map(lambda x:self.wordsmap[x],\
                    keywordset)
            manualkeywords[docname] = set(keywordset)
        return manualkeywords

    def mkfeatures(self):
        corpfeature = {}
        for dockey in self.doctext.keys():
            docfeature = {}
            doctext = self.doctext[dockey]
            doctags = self.doctags[dockey]
            for i, word in enumerate(doctext):
                if word in self.wordsmap and doctags[i] in self.posset:
                    if self.wordsmap[word] not in docfeature:
                        # class
                        #wordfeature = Feature()
                        #wordfeature.tf  = 1
                        #wordfeature.df = self.worddf[word]
                        #wordfeature.position = i
                        # list
                        wordfeature = [0 for j in range(self.featurenum)]
                        wordfeature[0] = 1
                        wordfeature[1] = self.worddf[self.wordsmap[word]]
                        wordfeature[2] = i
                        # word's length feature
                        if self.feature_bittag[4] == 1:
                            #wordfeature.lentext = len(word)
                            wordfeature[4] = len(word)
                        # word's pos feature
                        if self.feature_bittag[5] == 1:
                            posidx = self.poslist.index(doctags[i])
                            if posidx < 0:
                                print 'Invalid pos tags'
                                sys.exit(1)
                            wordfeature[self.nonposfeature+posidx] = 1
                        docfeature[self.wordsmap[word]] = wordfeature
                    else:
                        docfeature[self.wordsmap[word]][0] += 1
            # word's tfidf feature
            if self.feature_bittag[3] == 1:
                for wordkey in docfeature.keys():
                    docfeature[wordkey][3] = self.comptfidf(\
                            docfeature[wordkey][0], docfeature[wordkey][1],\
                            len(self.doctext.keys()))
            corpfeature[dockey] = docfeature
        return corpfeature

    def comptfidf(self, tf, df, docnum):
        return tf*math.log((docnum*1.0)/df)

    def normalization(self, method):
        ''' feature normalization:
            1.document frequency features are normalized
            in the whole corpus;
            2.words frequency and position are normalized
            in their corresponding document.
        '''
        if method == 'minmax':
            self.minmax()
        elif method == 'norm':
            self.norm()
        elif method == 'original':
            pass
        else:
            print 'Invalid method choice'
            sys.exit(0)

    def minmax(self):
        std_feature = {}
        # words' df feature
        mindf = min(map(lambda x:x[1], self.worddf.items()))
        maxdf = max(map(lambda x:x[1], self.worddf.items()))
        for dockey in self.corpfeature.keys():
            docfeature = self.corpfeature[dockey]
            mintf = min(map(lambda x:x[1][0],\
                    docfeature.items()))
            maxtf = max(map(lambda x:x[1][0],\
                    docfeature.items()))
            minpos = min(map(lambda x:x[1][2],\
                     docfeature.items()))
            maxpos = max(map(lambda x:x[1][2],\
                     docfeature.items()))
            if self.feature_bittag[3] == 1:
                mintfidf = min(map(lambda x:x[1][3],\
                           docfeature.items()))
                maxtfidf = max(map(lambda x:x[1][3],\
                           docfeature.items()))
            if self.feature_bittag[4] == 1:
                minlength = min(map(lambda x:x[1][4],\
                            docfeature.items()))
                maxlength = max(map(lambda x:x[1][4],\
                            docfeature.items()))
            for word in docfeature.keys():
                docfeature[word][0] = 1.0*(docfeature[word][0]-mintf)\
                        /max(1, (maxtf-mintf))
                docfeature[word][1] = 1.0*(docfeature[word][1]-mindf)\
                        /(maxdf-mindf)
                docfeature[word][2] = 1.0*(docfeature[word][2]-minpos)\
                        /(maxpos-minpos)
                if self.feature_bittag[3] == 1:
                    docfeature[word][3] = 1.0*(docfeature[word][3]-mintfidf)\
                        /(maxtfidf-mintfidf)
                if self.feature_bittag[4] == 1:
                    docfeature[word][4] = 1.0*(docfeature[word][4]-minlength)\
                        /(maxlength-minlength)

            std_feature[dockey] = docfeature
        self.corpfeature = std_feature

    def norm(self):
        pass

    def outputdocfeatures(self):
        for dockey in self.corpfeature.keys():
            docfeature = self.corpfeature[dockey]
            manuallabelkey = dockey.split('/')[-1].split('.')[0]
            if dockey.find('Train') != -1:
                dir_feature = self.dir_feature[0]
            elif dockey.find('Validation') != -1:
                dir_feature = self.dir_feature[1]
            elif dockey.find('Test') != -1:
                dir_feature = self.dir_feature[2]
            else:
                dir_feature = self.dir_feature[0]
            output_feature_file = dir_feature\
                    + manuallabelkey + '.' + self.feature_suffix
            wfd = open(output_feature_file, 'w')
            for word in docfeature.keys():
                #print word
                #print self.manualkeywords[manuallabelkey]
                #raw_input()
                if word in self.manualkeywords[manuallabelkey]:
                    wfd.write('%s 1 %f %f %f' % (word,\
                        docfeature[word][0], docfeature[word][1],\
                        docfeature[word][2]))
                else:
                    wfd.write('%s 0 %f %f %f' % (word,\
                        docfeature[word][0], docfeature[word][1],\
                        docfeature[word][2]))
                if self.feature_bittag[3] == 1:
                    wfd.write(' %f' % docfeature[word][3])
                if self.feature_bittag[4] == 1:
                    wfd.write(' %f' % docfeature[word][4])
                if self.feature_bittag[5] == 1:
                    for i in range(5, self.featurenum):
                        wfd.write(' %d' % docfeature[word][i])
                wfd.write('\n')
            wfd.close()

class Feature:
    '''This class plays a role of structure
    '''
    def __init__(self):
        tf    = 0.0
        df   = 0.0
        position = 0.0
        tfidf = 0.0
        lentext  = 0.0
        postag = [0 for i in range(len(TOPIC_POS))]


def main():
    # choice of node to be processed
    #word_choice = "NounAdj"
    word_choice = "AllPos"

    # feature choice
    nonposfeature = 3
    feature_bittag = [1, 1, 1, 0, 0, 1]

    # file path setting(need manual modifying for different methods)
    dir_text = ['../cleanData/Hulth2003/Train/',\
                '../cleanData/Hulth2003/Validation/',\
                '../cleanData/Hulth2003/Test/']
    text_suffix = 'abstr'
    dir_feature = ['../features/rankSvm/Train/',\
                   '../features/rankSvm/Validation/',\
                   '../features/rankSvm/Test/']
    feature_suffix = 'feature'
    dir_manualkp = ['../cleanData/Hulth2003/Train/',\
                    '../cleanData/Hulth2003/Validation/',\
                    '../cleanData/Hulth2003/Test/']
    manualkp_suffix = 'keyword'

    if word_choice == 'NounAdj':
        wordsmap_file = '../cleanData/Hulth2003/words_map.clean.dict'
        posset = POS
    elif word_choice == 'AllPos':
        wordsmap_file = '../cleanData/Hulth2003/words_map.complete.dict'
        posset = TOPIC_POS
    else:
        print 'Invalid word choice'
        sys.exit(1)

    featurenum = nonposfeature + len(posset)
    featureGenerator = NodeFeatureGenerator(posset, feature_bittag,\
            dir_text, text_suffix, dir_feature, feature_suffix, dir_manualkp,\
            manualkp_suffix, wordsmap_file, featurenum, nonposfeature)
    featureGenerator.generatefeature('minmax')

if __name__ == "__main__":

    main()
