import urllib3
from bs4 import BeautifulSoup
import os

http = urllib3.PoolManager()


def checkDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

outputdirname = "setopatioutput"
setopatiurl = "http://setopati.com/bichar/"

checkDir(outputdirname)

# make sure the output directory exist
# iterate through the news artices.
for i in range(2000, 12000):
    filename = os.path.join(outputdirname, str(i))

    # if the output file for the news article already exist, skip it.
    # this will prevent us from redoing much task if the script gets broken in the
    # middle of extraction.
    if os.path.exists(filename):
        print("Skipping ", i)
        continue
    # try to get the HTML content of the URL
    articleurl = setopatiurl+str(i)
    print("Extracting content from ", i)
    r = http.request('GET', articleurl)

    # create a file
    outputfile = open(filename, 'wb')
    if r.status == 200:
        # success. Now try to extract the news portition using beautifulsoup
        extractor = BeautifulSoup(r.data)
        # the content inside division with ID 'newsbox' is the main content
        newsbox = extractor.find("div", {"id": "newsbox"})
        if len(newsbox) > 1:
            # if there is news inside the news box, then it's length will be > 1
            # remove the content inside span, h1, h2 etc
            for htmltag in ['strong', 'h1', 'h2']:
                for tag in newsbox.find_all(htmltag):
                    tag.decompose()
            content = bytes(newsbox.get_text(), 'UTF-8')
            outputfile.write(bytes(' ', 'UTF-8').join(content.split(bytes('\n', 'UTF-8'))))

    outputfile.close()
