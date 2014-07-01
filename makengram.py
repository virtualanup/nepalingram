# makengram.py
# script to make ngram models from the raw text
# by Anup pokhrel
# http://virtualanup.com

from collections import defaultdict

class ngrammodel:
    def __init__(self,n):
        '''Constructor for the ngram model generator
        n is the model number like 1 for unigram,
        2 for bigram and so on'''
        self.n = n
        self.words = defaultdict(int) # words are stored as a dictionary

    def processarticle(self,article):
        '''
        process a single article.
        the function will split the article into sentences and
        process the sentences
        '''
        # There is not simple way of representing a word in regex in nepali language
        # so, we can simply assume the text to be split into sentences seperated by
        # some symbols. We will then process the sentence

        # endsymbols represent the symbols used to end sentences
        endsymbols = ['?','!','.',';']
        for symbol in endsymbols:
            article.replace(symbol,'।') #replace with end of sentence symbol
        sentences = article.split('।')
        for sentence in sentences:
            self.processsentence(sentence)

    def processsentence(self,sentence):
        '''
        process the sentence. It splits the sentence into words and analyze the word list
        '''
        endsymbols = ['-',',','\'','"','\t']
        for symbol in endsymbols:
            sentence.replace(symbol,' ')
        words = sentence.split(' ')
        for word in words:
            self.words[word] += 1
        
    def readfile(self,file):
        '''
        reads the content of the file and saves in the ngram
        model
        '''
        for line in file:
            self.processarticle(line)

    def saveoutput(self,file):
        '''
        saves the output in the given file
        '''
        for word in sorted(self.words, key=self.words.get, reverse=True):
            validletters=['क','ख',u'ग',u'घ',u'ङ',u'च',u'छ',u'ज',u'झ',u'ञ',u'ट',u'ठ',u'ड',u'ढ',u'ण',u'त',u'थ',u'द',u'ध',u'न',u'प',u'फ',u'ब',u'भ',u'म',u'य',u'र',u'ल',u'व',u'श',u'ष',u'स',u'ह',u'अ',u'आ',u'इ',u'ई',u'उ',u'ऊ',u'ए',u'ऐ',u'ओ',u'औ',u'अ',u'अ',u'०',u'१',u'२',u'३',u'४',u'५',u'६',u'७',u'८',u'९']
            # at least one of the avove letters must occur at least once in the text
            # to be considered as a valid word
            for letter in validletters:
                if letter in word:
                    file.write(word+' '+str(self.words[word])+"\n")
                    break
