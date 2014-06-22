#!/usr/bin/python3
from bs4 import BeautifulSoup
import urllib3
import os

http = urllib3.PoolManager()


def checkDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

outputdirname = "nagariknewsoutput"
nagariknewsurl = "http://nagariknews.com/politics/story/"
# make sure the output directory exist
checkDir(outputdirname)

# iterate through the news artices.
for i in range(1343, 20000):
    filename = os.path.join(outputdirname, str(i))

    # if the output file for the news article already exist, skip it.
    # this will prevent us from redoing much task if the script gets broken in the
    # middle of extraction.
    if os.path.exists(filename):
        print(i,"th file already exists. Skipping it...")
        continue
    #this is a line and the main purpose of the file is to consider th
    # try to get the HTML content of the URL
    articleurl = nagariknewsurl + str(i)
    print("Extracting content from new id ", i)
    r = http.request('GET', articleurl)

    # create a file
    outputfile = open(filename, 'wb')
    if r.status == 200:
        try:
            # success. Now try to extract the news portition using beautifulsoup
            extractor = BeautifulSoup(r.data)
            # the content inside division with ID 'newsbox' is the main content
            introtext = extractor.find("div", {"class": "itemIntroText"})
            fulltext = extractor.find("div", {"class": "itemFullText"})
            content = ''
            if introtext is not None and fulltext is not None:
                content = bytes(introtext.get_text(), 'UTF-8')
                content += bytes(fulltext.get_text(), 'UTF-8')
            outputfile.write(bytes(' ', 'UTF-8').join(content.split(bytes('\n', 'UTF-8'))))
        except:
            pass # do nothing in case of exception. Just skip that URL

    outputfile.close()
