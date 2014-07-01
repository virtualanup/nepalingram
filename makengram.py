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
        endsymbols = ['?','!','.',';','\n']
        for symbol in endsymbols:
            article.replace(symbol,'।') #replace with end of sentence symbol
        sentences = article.split('।')
        for sentence in sentences:
            # sentence must be of enough length
            if len(sentence) > 10:
                self.processsentence(sentence)

    def processsentence(self,sentence):
        '''
        process the sentence. It splits the sentence into words and analyze the word list
        '''
        endsymbols = ['-',',','\'','"','\t']
        for symbol in endsymbols:
            sentence.replace(symbol,' ')
        if self.n > 1:
            # record the start and end of sentences by a chinese letter (to make
            # sure it won't exist in text data
            words = ['西']+sentence.split(' ')+['西']
        else:
            words = sentence.split(' ')

        wordlist = []
        for word in words:
            # to meet the requirements of being a word, some of the predefined characters
            # must appear in it
            validletters=['क','ख',u'ग',u'घ',u'ङ',u'च',u'छ',u'ज',u'झ',u'ञ',u'ट',u'ठ',u'ड',u'ढ',u'ण',u'त',u'थ',u'द',u'ध',u'न',u'प',u'फ',u'ब',u'भ',u'म',u'य',u'र',u'ल',u'व',u'श',u'ष',u'स',u'ह',u'अ',u'आ',u'इ',u'ई',u'उ',u'ऊ',u'ए',u'ऐ',u'ओ',u'औ',u'अ',u'अ',u'०',u'१',u'२',u'३',u'४',u'५',u'६',u'७',u'८',u'९','西']
            
            for letter in validletters:
                if letter in word:
                    wordlist.append(word)
                    if(len(wordlist) == self.n):
                        self.words[' '.join(wordlist)] += 1
                        wordlist = wordlist[1:]
                    break # break to next word
        
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
        for wordseq in sorted(self.words, key=self.words.get, reverse=True):
            file.write(wordseq+' '+str(self.words[wordseq])+"\n")
