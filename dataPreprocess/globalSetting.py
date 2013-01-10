#!/usr/bin/env python
#encoding=utf8

# Only considering the following part of speech tag in semantic graph
POS = set(['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS'])

# Saving the following POS when computing topic distribution
TOPIC_POS = set(['CD', 'FW', 'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', \
        'NNPS', 'PRP', 'RB', 'RBR', 'RBS', 'UH', 'VB', 'VBD', 'VBG', \
        'VBN', 'VBP', 'VBZ'])

# Remove words without number of letter
REG_EXP = r".*[a-zA-Z].*"

# Web service address
WEB_SERVICE_COMPARE = "http://166.111.68.55:8000/wikipediaminer\
        /services/compare"

# Commander
CMD = "~/Doctor/Code/ModelCode/Topic\ Model/LDA/C++-Gibbs/GibbsLDA++-0.2/src/lda \
        -est -beta 0.1 "

# Stopwords file
STOPWORDS_FILE = "../../data/en-stopwords.txt"

# Stopwords processing
class Stopwords:
    ''' responsible for stopwords related operations,
        minaly including scaning.
    '''
    def __init__(self):
        self.stopwords = set([])
        self.loaddata()

    def loaddata(self):
        for line in open(STOPWORDS_FILE):
            word = line.strip("\n")
            self.stopwords.add(word)

    def is_stopword(self, word):
        if word in self.stopwords:
            return True
        return False
