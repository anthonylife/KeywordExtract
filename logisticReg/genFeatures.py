#!/usr/bin/env python
#encoding=utf8

'''
Author : anthonylife
Date   : 1/15/2013
'''
import numpy as np
import sys, os
sys.path.append('../')

from dataPreprocess.filterWords import WordFilter
from stemmer.porterStemmer import PorterStemmer

class FeatureGenerator():
    '''This class serves for the supervised keyphrase
       extraction method, i.e., logistic regression
       for keyword extraction and then merge keywords
       to keyphrases.
       Features: as we use "POS tags" to merge keywords
       when generating keyphrases, we don't use "POS" tags as features,
            1.TF;
            2.DF;
            3.POSITION.
       Note: all features should be normalized.
    '''
    def __init__(self, dir_text_file, text_suffix,\
            dir_feature_file, feature_suffix,\
            dir_manualkp_file, manualkp_suffix,\
            words_map_file):
        self.dir_text_file = dir_text_file
        self.text_suffix = text_suffix
        self.dir_feature_file = dir_feature_file
        self.feature_suffix = feature_suffix
        self.dir_manualkp_file = dir_manualkp_file
        self.manualkp_suffix = manualkp_suffix
        self.words_map_file = words_map_file

        self.featurenum = 3

        self.stemmer = PorterStemmer()
        self.wordmap = self.loadmap()
        self.doclist = self.getdoclist(self.substr_text,\
                dir_text_file)
        self.wordFilter = WordFilter()
        self.doctext, self.worddf = self.loaddoctext()
        self.manualkeywords = self.getmanuallabels()
        corpfeature = self.mkdocfeatures()
        self.corpfeature = self.normalization(corpfeature,\
                method='minmax')

    def loaddoctext(self):
        doctext = {}
        worddf = {}
        for doc in self.doclist:
            docwordlist = []
            docwordset = set([])
            for line in open(doc):
                clean_words = self.wordFilter.filterwords(\
                        line.strip('\r\n '))
                docwordlist += clean_words
            #docname = doc.split('/')[-1].split('.')[0]
            doctext[doc] = docwordlist
            for word in set(docwordlist):
                if word in self.wordmap:
                    wordid = self.wordmap[word]
                    if wordid not in docwordset:
                        if wordid in worddf:
                            worddf[wordid] += 1
                        else:
                            worddf[wordid] = 1
                        docwordset.add(wordid)
        return doctext, worddf

    def getmanuallabels(self):
        '''segment each keyphrase into keywords
        '''
        manualkeywords = {}
        doclist = self.getdoclist(self.substr_manualkp,\
                self.dir_manualkp_file)
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
            keywordset = map(lambda x:self.wordmap[x],\
                    keywordset)
            manualkeywords[docname] = set(keywordset)
        return manualkeywords

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

    def loadmap(self):
        wordsmap = {}
        for line in open(self.words_map_file):
            biparts = line.strip('\n').split(' ')
            wordsmap[biparts[0]] = biparts[1]
        return wordsmap

    def mkdocfeatures(self):
        '''Feature format:
            1.tf; 2.df; 3.position
        '''
        corpfeature = {}
        for key in self.doctext.keys():
            docfeature = {}
            doctext = self.doctext[key]
            for i, word in enumerate(doctext):
                if word in self.wordmap:
                    if self.wordmap[word] not in docfeature:
                        docfeature[self.wordmap[word]] = \
                            [1, self.worddf[self.wordmap[word]], i]
                    else:
                        docfeature[self.wordmap[word]][0] += 1
            corpfeature[key] = docfeature
        return corpfeature

    def outputdocfeatures(self):
        for dockey in self.corpfeature.keys():
            docfeature = self.corpfeature[dockey]
            manuallabelkey = dockey.split('/')[-1].split('.')[0]
            if dockey.find('Train') != -1:
                dir_feature_file = self.dir_feature_file[0]
            elif dockey.find('Validation') != -1:
                dir_feature_file = self.dir_feature_file[1]
            elif dockey.find('Test') != -1:
                dir_feature_file = self.dir_feature_file[0]
            else:
                dir_feature_file = self.dir_feature_file[0]
            output_feature_file = dir_feature_file\
                    + manuallabelkey + '.' + self.feature_suffix
            wfd = open(output_feature_file, 'w')
            for word in docfeature.keys():
                #print word
                #print self.manualkeywords[manuallabelkey]
                #raw_input()
                if word in self.manualkeywords[manuallabelkey]:
                    wfd.write('%s 1 %f %f %f\n' % (word,\
                        docfeature[word][0], docfeature[word][1],\
                        docfeature[word][2]))
                else:
                    wfd.write('%s 0 %f %f %f\n' % (word,\
                        docfeature[word][0], docfeature[word][1],\
                        docfeature[word][2]))
            wfd.close()

    def normalization(self, features, method):
        ''' feature normalization:
            1.document frequency features are normalized
            in the whole corpus;
            2.words frequency and position are normalized
            in their corresponding document.
        '''
        if method == 'minmax':
            features = self.minmax(features)
        elif method == 'norm':
            features = self.norm(features)
        elif method == 'original':
            pass
        else:
            print 'Invalid method choice'
            sys.exit(0)
        return features

    def minmax(self, features):
        std_feature = {}
        #mindf = min(map(lambda x:x[1], self.worddf.items()))
        #maxdf = max(map(lambda x:x[1], self.worddf.items()))
        maxdf = 3
        mindf = 1
        for dockey in features.keys():
            docfeature = features[dockey]
            mintf = min(map(lambda x:x[1][0],\
                    docfeature.items()))
            maxtf = max(map(lambda x:x[1][0],\
                    docfeature.items()))
            minpos = min(map(lambda x:x[1][2],\
                    docfeature.items()))
            maxpos = max(map(lambda x:x[1][2],\
                    docfeature.items()))
            for word in docfeature.keys():
                docfeature[word][0] = 1.0*(docfeature[word][0]-mintf)\
                        /max(1, (maxtf-mintf))
                docfeature[word][1] = 1.0*(docfeature[word][1]-mindf)\
                        /(maxdf-mindf)
                docfeature[word][2] = 1.0*(docfeature[word][2]-minpos)\
                        /(maxpos-minpos)
            std_feature[dockey] = docfeature
        return std_feature

    def norm(self, features):
        meandf = np.mean(np.array(map(lambda x:x[1],\
                self.worddf.items())))
        stddf = np.std(np.array(map(lambda x:x[1],\
                self.worddf.items())))
        for dockey in features.keys():
            docfeature = features[dockey]
            meantf = np.mean(np.array(map(lambda x:x[1][0],\
                    docfeature.items())))
            stdtf = np.std(np.array(map(lambda x:x[1][0],\
                    docfeature.items())))
            meanpos = np.mean(np.array(map(lambda x:x[1][2],\
                    docfeature.items())))
            stdpos = np.std(np.array(map(lambda x:x[1][2],\
                    docfeature.items())))
            for word in docfeature.keys():
                docfeature[word][0] = (docfeature[word][0]-meantf)\
                        / stdtf
                docfeature[word][1] = (docfeature[word][1]-meandf)\
                        / stddf
                docfeature[word][2] = (docfeature[word][2]-meanpos)\
                        / stdpos
            features[dockey] = docfeature
        return features


def test():
    dir_text_file = ['../unitTest/logisticReg/']
    text_suffix = 'abstr'
    dir_feature_file = ['../unitTest/logisticReg/']
    feature_suffix = 'feature'
    dir_manualkp_file = ['../unitTest/logisticReg/']
    manualkp_suffix = 'keyword'
    words_map_file = '../cleanData/Hulth2003/words_map.clean.dict'
    featureGenerator = FeatureGenerator(dir_text_file,\
            text_suffix, dir_feature_file, feature_suffix,\
            dir_manualkp_file, manualkp_suffix,\
            words_map_file)
    featureGenerator.outputdocfeatures()

def main():
    dir_text_file = ['../cleanData/Hulth2003/Train/',\
            '../cleanData/Hulth2003/Validation/',\
            '../cleanData/Hulth2003/Test/']
    text_suffix = 'abstr'
    dir_feature_file = ['../features/logisticReg/Train/',\
            '../features/logisticReg/Validation/',\
            '../features/logisticReg/Test/']
    feature_suffix = 'feature'
    dir_manualkp_file = ['../cleanData/Hulth2003/Train/',\
            '../cleanData/Hulth2003/Validation/',\
            '../cleanData/Hulth2003/Test/']
    manualkp_suffix = 'keyword'
    words_map_file = '../cleanData/Hulth2003/words_map.clean.dict'

    featureGenerator = FeatureGenerator(dir_text_file,\
            text_suffix, dir_feature_file, feature_suffix,\
            dir_manualkp_file, manualkp_suffix,\
            words_map_file)
    featureGenerator.outputdocfeatures()

if __name__ == "__main__":
    #test()
    main()
