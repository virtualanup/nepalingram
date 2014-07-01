#!/usr/bin/python3
# program to join the contents of a directory into a single file
# for Nepali ngram model
# http://virtualanup.com


import os, os.path

def makesinglefile(directory,filename):
    '''
    Function to read all the files in a directory
    and add the contents of all the files in the directory
    to a single file'''

    outputfile = open(filename,"w")
    for root, _, files in os.walk(directory):
        for f in files:
            fullpath = os.path.join(root, f)
            print("Processing ",fullpath)
            #open the file and read the contents
            content = open(fullpath).read()
            outputfile.write(content)
            outputfile.write('\n')

makesinglefile('nagariknewsoutput','nagariksingle')
makesinglefile('setopatioutput','setopatisingle')
