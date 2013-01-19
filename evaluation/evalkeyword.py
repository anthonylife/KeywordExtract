#!/usr/bin/env python
#encoding=utf8

'''
@Author : anthonylife
@Date   : 1/20/2013
'''

import os, sys
sys.path.append('../')

from stemmer.porterStemmer import PorterStemmer

class EvalResult:
    '''This class is used to evalute the results of keywords extraction.
       Currently, I adopt Precision@K and F-score to evaluate.
       In the keywords extraction task, we only consider words occured
       in the text.
    '''
    def __init__(self, wordsmap_file, dir_keywords, dir_result, topk, \
            keywords_suffix, result_suffix, completekwnum_suffix):
        self.wordsmap_file   = wordsmap_file
        self.dir_keywords    = dir_keywords
        self.dir_result      = dir_result
        self.keywords_suffix = keywords_suffix
        self.result_suffix   = result_suffix
        self.topk            = topk
        self.completekwnum_suffix = completekwnum_suffix

        self.stemmer  = PorterStemmer()
        self.wordsmap = self.loadmap()
        self.manualkeywords  = self.getmanualkeywords()
        self.extractkeywords = self.self.getextractkeywords()

    def getdoclist(self, dir_file, filter_func):
        doclist = []
        candi_files = os.listdir(dir_file)
        # filter file by suffix if existed
        candi_files = filter(filter_func, candi_files)
        candi_files = map(lambda x: dir_file+x, candi_files)
        doclist = doclist + candi_files
        return doclist

    def loadmap(self):
        wordsmap = {}
        for line in open(self.wordsmap_file):
            biparts = line.strip('\n').split(' ')
            wordsmap[biparts[0]] = biparts[1]
        return wordsmap

    def substr_keywords(self, candi_file):
        if candi_file.find(self.keywords_suffix) != -1:
            return True
        return False
    def substr_results(self, candi_file):
        if candi_file.find(self.result_suffix) != -1:
            return True
        return False
    def substr_kwnum(self, candi_file):
        if candi_file.find(self.completekwnum_suffix) != -1:
            return True
        return False

    def getmanualkeywords(self):
        '''Get manual keywords occured in the text.
        '''
        doclist = self.getdoclist(self.dir_keywords, self.substr_keywords)
        manuallabels = {}
        for doc in doclist:
            docname = doc.split('/')[-1].split('.')[0]
            keywords_set = set([])
            for line in open(doc):
                words = line.strip('\r\n ').split(' ')
                for word in words:
                    word = word.lower()
                    word = self.stemmer.stem(word, 0, len(word)-1)
                    if word not in self.wrodsmap:
                        print 'Invalid keyword'
                        sys.exit(0)
                    word_id = self.wordsmap[word]
                    keywords_set.add(word_id)
            manuallabels[docname] = keywords_set
        return manuallabels

    def getextractkeywords(self):
        '''Get the extracted keywords accroding to the ranking value
           of candidate keywords.
        '''
        doclist = self.getdoclist(self.dir_result, self.substr_results)
        extractkeywords = {}
        for doc in doclist:
            docname = doc.split('/')[-1].split('.')[0]
            tempwords = []
            for line in open(doc):
                biparts = line.strip('\n\r ').split(' ')
                tempwords.append([biparts[0], float(biparts[1])])
            tempwords = sorted(tempwords, key=lambda x: x[1],reverse=True)
            sortedwords = map(lambda x: x[0], tempwords)
            dockeywords = set(sortedwords[0:self.topk])
            extractkeywords[docname] = dockeywords
        return extractkeywords

    def evaluation(self, eval_choice=None):
        if eval_choice == 'F-score':
            precision, recall, f_score = self.eval_fscore()
            print 'Precision: %f, Recall: %f, F-score: %f\n'\
                    % (precision, recall, f_score)
        elif eval_choice == 'Bpref':
            bpref = self.eval_bpref()
            print 'Bpref: %f\n' % bpref
        elif eval_choice == 'MRR':
            mrr = self.eval_mrr()
            print 'Mrr: %f\n' % mrr
        else:
            precision, recall, f_score = self.eval_fscore()
            bpref = self.eval_bpref()
            mrr = self.eval_mrr()
            print 'Precision: %f, Recall: %f, F-score: %f\n'\
                    % (precision, recall, f_score)
            print 'Bpref: %f\n' % bpref
            print 'Mrr: %f\n' % mrr

    # Using F-score to evaluate
    def eval_fscore(self):
        total_accnum = 0
        ext_accnum = 0
        ext_num = 0
        for doc in self.manualkeywords.keys():
            manual_kw  = self.manualkeywords[doc]
            ext_kw = self.extractkeywords[doc]
            total_accnum += len(manual_kw)
            ext_num += len(ext_kw)
            ext_accnum += len(manual_kw&ext_kw)
        print 'Manual annotated keyphrases: %d' % total_accnum
        print 'Extracted total keyphrases: %d' % ext_num
        print 'Extracted accurate keyphrases: %d' % ext_accnum
        precision = ext_accnum*1.0/ext_num
        recall = ext_accnum*1.0/total_accnum
        fscore = 2*precision*recall/(precision+recall)
        return precision, recall, fscore

    # Using MRR to evaluate
    def eval_mrr(self):
        pass

    # Using Bpref to evaluate
    def eval_bpref(self):
        pass


