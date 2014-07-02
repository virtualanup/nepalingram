#!/usr/bin/python3
# makengram.py
# script to make ngram models from the raw text
# by Anup pokhrel
# http://virtualanup.com/nepali-ngram-models/

from collections import defaultdict
import sys

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
            artice = article.replace(symbol,'।') #replace with end of sentence symbol
        sentences = article.split('।')
        for sentence in sentences:
            # sentence must be of enough length
            if len(sentence) > 10:
                self.processsentence(sentence)

    def processsentence(self,sentence):
        '''
        process the sentence. It splits the sentence into words and analyze the word list
        '''
        endsymbols = ['-',',','\'','"','\t','(',')','<','>','‘','’','“','”','–']
        for symbol in endsymbols:
            sentence = sentence.replace(symbol,' ')
        if self.n > 1:
            # record the start and end of sentences by #
            words = ['#']+sentence.split(' ')+['#']
        else:
            words = sentence.split(' ')

        wordlist = []
        for word in words:
            # to meet the requirements of being a word, some of the predefined characters
            # must appear in it
            validletters=['क','ख','ग','घ','ङ','च','छ','ज','झ','ञ','ट','ठ','ड','ढ','ण','त','थ','द','ध','न','प','फ','ब','भ','म','य','र','ल','व','श','ष','स','ह','अ','आ','इ','ई','उ','ऊ','ए','ऐ','ओ','औ','अ','अ','०','१','२','३','४','५','६','७','८','९','#']
            
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

if __name__ == '__main__':
    # get the model number from command line
    # like ./makengram.py 2 <outputfilename> for bigram model
    if len(sys.argv) != 3:
        print("Syntax : "+sys.argv[0]+" <model_number> <output_file>",len(sys.argv))
        exit()
    mn = int(sys.argv[1])
    if mn<1 or mn> 5:
        print("Model number not supported")
        exit()
    model = ngrammodel(mn)
    #model.readfile(open('test'))
    model.readfile(open('setopatisingle'))
    model.readfile(open('nagariksingle'))
    model.saveoutput(open(sys.argv[2],'w+'))
