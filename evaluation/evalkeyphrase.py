#!/usr/bin/env python
#encoding=utf8

# Details: More description about evaluation on this task
#          is represented in the "README" file.
#
# Author : anthonylife
# Date   : 1/13/2012

import os, sys
sys.path.append('../')

from stemmer.porterStemmer import PorterStemmer
from dataPreprocess.globalSetting import ADJ_POS, NOUN_POS

class EvalResult:
    '''This class is responsible to do evaluation
       on the extraction results.
    '''
    def __init__(self, words_map_file, dir_keywords_file,\
            dir_results_file, dir_wholetext_file,\
            keywords_suffix, results_suffix, wholetext_suffix,\
            kwnum_suffix, topk):
        self.words_map_file = words_map_file
        self.dir_keywords_file = dir_keywords_file
        self.dir_results_file = dir_results_file
        self.dir_wholetext_file = dir_wholetext_file
        self.keywords_suffix = keywords_suffix
        self.results_suffix = results_suffix
        self.wholetext_suffix = wholetext_suffix
        self.kwnum_suffix = kwnum_suffix
        self.topk = topk

        self.stemmer = PorterStemmer()
        self.wordsmap = self.loadmap()
        self.doclist = self.getdoclist(self.dir_wholetext_file,\
                self.substr_wholetext)

        self.corpkeyphrase = {}
        self.getkeyphrase()
        self.manualkwnum = {}
        self.manuallabels = {}
        self.getmanuallabels()

    def getdoclist(self, dir_file, filter_func):
        doclist = []
        candi_files = os.listdir(dir_file)
        # filter file by suffix if existed
        candi_files = filter(filter_func, candi_files)
        candi_files = map(lambda x: dir_file+x, candi_files)
        doclist = doclist + candi_files
        return doclist

    def substr_keywords(self, candi_file):
        if candi_file.find(self.keywords_suffix) != -1:
            return True
        return False
    def substr_results(self, candi_file):
        if candi_file.find(self.results_suffix) != -1:
            return True
        return False
    def substr_wholetext(self, candi_file):
        if candi_file.find(self.wholetext_suffix) != -1:
            return True
        return False
    def substr_kwnum(self, candi_file):
        if candi_file.find(self.kwnum_suffix) != -1:
            return True
        return False

    def loadmap(self):
        wordsmap = {}
        for line in open(self.words_map_file):
            biparts = line.strip('\n').split(' ')
            wordsmap[biparts[0]] = biparts[1]
        return wordsmap

    def getkeyphrase(self):
        for doc in self.doclist:
            results_file = self.dir_results_file \
                    + doc.split('/')[-1].split('.')[0]\
                    + '.' + self.results_suffix
            #print results_file
            #print doc
            docwordlist = []
            docwordtags = []
            for line in open(doc):
                line = line.strip("\n\r ")
                save_words, save_postags = self.filterwords(line)
                docwordlist = docwordlist + save_words
                docwordtags = docwordtags + save_postags

            dockeywords, sortedwords, wordsvalue = \
                    self.getkeywords(results_file)
            #print sortedwords
            kp_num, dockeyphrase = self.mergekeywords(dockeywords,\
                    docwordlist, wordsvalue, docwordtags)
            #print dockeyphrase
            #print dockeyphrase
            #raw_input()
            dockeyphrase = sorted(dockeyphrase.items(), \
                    key=lambda x:x[1], reverse=True)
            dockeyphrase = map(lambda x:x[0], dockeyphrase)
            self.corpkeyphrase[doc.split('/')[-1].split('.')[0]] = \
                    set(dockeyphrase[0:int(10.0*len(dockeyphrase)/10+1)+1])

    def getmanuallabels(self):
        doclist = self.getdoclist(self.dir_keywords_file,\
                self.substr_kwnum)
        for doc in doclist:
            docname = doc.split('/')[-1].split('.')[0]
            manual_kwnum = int(open(doc).readline().strip('\n'))
            self.manualkwnum[docname] = manual_kwnum

        doclist = self.getdoclist(self.dir_keywords_file,\
                self.substr_keywords)
        for doc in doclist:
            docname = doc.split('/')[-1].split('.')[0]
            keyphrase_set = set([])
            for line in open(doc):
                words_id =[]
                words = line.strip('\r\n ').split(' ')
                for word in words:
                    word = word.lower()
                    word = self.stemmer.stem(word, 0, \
                        len(word)-1)
                    if word not in self.wordsmap:
                        print 'Invalid keyword'
                        sys.exit(0)
                    word_id = self.wordsmap[word]
                    words_id.append(word_id)
                keyphrase = '_'.join(words_id)
                keyphrase_set.add(keyphrase)
            self.manuallabels[docname] = keyphrase_set

    def mergekeywords(self, dockeywords, docwordlist, wordsvalue,\
            docwordtags):
        dockeyphrase = {}
        kp_num = 0
        kp_tag = False
        kp_start = 0
        for i,word in enumerate(docwordlist):
            if not kp_tag:
                if word in dockeywords:
                    kp_start = i
                    kp_tag = True
            else:
                if word not in dockeywords or i == len(docwordlist)-1:
                    kp_end = i if word not in dockeywords else i+1
                    kp_tag = False
                    keywords_segment = docwordlist[kp_start:kp_end]
                    keywords_postags = docwordtags[kp_start:kp_end]
                    keywords_segment = self.postag_verify(keywords_segment,\
                            keywords_postags)
                    if keywords_segment:
                        keyphrase = '_'.join(keywords_segment)
                        keyphrase_val = self.getkpvalue(keywords_segment,\
                                wordsvalue)
                        if keyphrase not in dockeyphrase:
                            dockeyphrase[keyphrase] = keyphrase_val
                            kp_num += 1
        return kp_num, dockeyphrase

    def getkpvalue(self, keywords_segment, wordsvalue):
        kpvalue = 0.0
        for keyword in keywords_segment:
            kpvalue += wordsvalue[keyword]
        return kpvalue

    def getkeywords(self, keywords_file):
        tempwords = []
        for line in open(keywords_file):
            biparts = line.strip('\n\r ').split(' ')
            tempwords.append([biparts[0], float(biparts[1])])
        tempwords = sorted(tempwords, key=lambda x: x[1],\
                reverse=True)
        #print tempwordss)
        sortedwords = map(lambda x: x[0], tempwords)
        #print sortedwords
        #raw_input()
        wordsvalue = dict(tempwords)
        wordsnum = len(sortedwords)
        keywordsnum = int(1.0*wordsnum)
        dockeywords = set(sortedwords[0:keywordsnum])
        return dockeywords, sortedwords, wordsvalue

    def filterwords(self, textline):
        save_words = []
        save_postags = []
        words = textline.split(" ")
        for word in words:
            biparts = word.split("_")
            if len(biparts) != 2:
                print 'Invalid words occurence.'
                sys.exit(0)
            # words processing (stemming, lower)
            # ============================================
            biparts[0] = biparts[0].lower()
            biparts[0] = self.stemmer.stem(biparts[0], 0, \
                    len(biparts[0])-1)
            # ============================================
            if biparts[0] not in self.wordsmap:
                save_words.append('-1')
                save_postags.append(biparts[1])
            else:
                save_words.append(self.wordsmap[biparts[0]])
                save_postags.append(biparts[1])
        return save_words, save_postags

    # filter candidate keyphrase with invalid postag sequence
    def postag_verify(self, save_words, save_postags):
        #if len(save_words) == 1 and save_postags[0] in ADJ_POS:
        #    return None
        return save_words

    '''def postag_verify(self, save_words, save_postags):
        state = 0
        end_idx = -1
        for i, postag in enumerate(save_postags):
            if state == 0:
                if postag in ADJ_POS:
                    continue
                elif postag in NOUN_POS:
                    state = 1
            elif state == 1:
                if postag in ADJ_POS:
                    end_idx = i-1
                elif postag in NOUN_POS:
                    end_idx = i
                    continue
        if end_idx == -1:
            return None
        else:
            return save_words[0:end_idx+1]
'''
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
        for doc in self.corpkeyphrase.keys():
            ext_kp = self.corpkeyphrase[doc]
            manual_kp = self.manuallabels[doc]
            #print ext_kp
            #print manual_kp
            #raw_input()
            #total_accnum += len(manual_kp)
            total_accnum += self.manualkwnum[doc]
            ext_num += len(ext_kp)
            ext_accnum += len(manual_kp&ext_kp)
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


def test():
    pass

# run this file alone with local setting
def localrun():
    words_map_file = '../cleanData/Hulth2003/words_map.clean.dict'
    dir_keywords_file = '../cleanData/Hulth2003/Test/'
    dir_results_file = '../result/randomWalk/'
    dir_wholetext_file = '../cleanData/Hulth2003/Test/'
    keywords_suffix = 'keyword'
    results_suffix = 'keyword.pv'
    wholetext_suffix = 'abstr'
    kwnum_suffix = 'integral.num'
    topk = 0

    evalResult = EvalResult(words_map_file, dir_keywords_file,\
            dir_results_file, dir_wholetext_file, keywords_suffix,\
            results_suffix, wholetext_suffix, kwnum_suffix, topk)
    evalResult.evaluation('F-score')

# run this class by terminal commander
def cmdrun():
    words_map_file = sys.argv[1]
    dir_keywords_file = [sys.argv[2]]
    dir_results_file = [sys.argv[3]]
    dir_wholetext_file = [sys.argv[4]]
    keywords_suffix = sys.argv[5]
    results_suffix = sys.argv[6]
    wholetext_suffix = sys.argv[7]
    kwnum_suffix = sys.artv[8]
    topk = int(sys.argv[9])

    evalResult = EvalResult(words_map_file, dir_keywords_file,\
            dir_results_file, dir_wholetext_file, keywords_suffix,\
            results_suffix, wholetext_suffix, kwnum_suffix, topk)
    evalResult.evaluation('F-score')

if __name__ == '__main__':
    #test()
    localrun()
    #cmdrun()
