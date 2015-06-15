#!/usr/bin/python3

from threading import Thread
import threading
from queue import Queue
import time
import requests
import re
import htmlParser

class rssArticle:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def set_text(self, inText):
        self.text = inText
 
    def get_text(self):
        return self.text

class downloadThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)  #start the thread

    #takes a url from the queue and sends it into the feedtoContent function
    #Then appends it to the article list variable
    def run(self):

        # This iterates once per web site 
        while True:

            # trying to get a new site to retreive
            # information from 
            with urlLock:  
                if not urlQueue.empty():
                    currentUrl = urlQueue.get()
                else:
                    # if there are no sites left in the queue, this 
                    # will break the main while loop, ending this
                    # thread
                    break

            homeHtml = requests.get(currentUrl).text
            items = homeHtml.split("<item>")
            items = items[1:]
            articles = []
 
            for i in items:
                title = i.split("<title>")[1].split("</title>")[0] 
                link = i.split("<link>")[1].split("</link>")[0] 
                ar = rssArticle(title, link)
                articles.append(ar)
   
            for a in articles:
                articleHtml = requests.get(a.get_url()).text
                articleText = htmlParser.get_paragraphs(articleHtml)
                a.set_text(articleText)
                time.sleep(3)

            with listLock:
                articleList.extend(articles) 

#setting the number of threads
THREAD_COUNT = 6


#retreiving urls from text file        
with open("url.txt") as f:
    urlList = f.read().split("\n")
    urlList = [x.strip() for x in urlList if len(x) > 0]
 
# a list with all of the threads for joining them later on
threadList = [] 
listLock = threading.Lock()
urlLock = threading.Lock()
  
urlQueue = Queue(len(urlList))

#filling queue with urls from file
for url in urlList:
    urlQueue.put(url)
 
#this will hold all of the contents taken from the articles
articleList = []
 
# starting threads
for i in range(THREAD_COUNT):
    thread = downloadThread()
    thread.start()
    threadList.append(thread)

# waiting for thread to be finished
for name in threadList:
    name.join() 

headlineText = ""
contentText = "" 
for i in articleList:
    headlineText = headlineText + i.get_title() + "\n"
    contentText = contentText + "<title>" + i.get_title() + ("</title>" + "\n" 
                  + "<article>" + i.get_text() + "</article>" + "\n")

    
#writing results to their respective files
with open("headline.txt", "w") as h:
    h.write(headlineText)
with open("content.txt", "w") as c:
    c.write(contentText)



