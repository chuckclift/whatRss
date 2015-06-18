#!/usr/bin/python3

from threading import Thread
import threading
from queue import Queue
import time
import requests
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
            with url_queue_lock:  
                if not url_queue.empty():
                    current_url = url_queue.get()
                else:
                    # if there are no sites left in the queue, this 
                    # will break the main while loop, ending this
                    # thread
                    break

            home_html = requests.get(current_url).text
            items = home_html.split("<item>")
            items = items[1:]
            articles = []
 
            for i in items:
                title = i.split("<title>")[1].split("</title>")[0] 
                link = i.split("<link>")[1].split("</link>")[0] 
                ar = rssArticle(title, link)
                articles.append(ar)
   
            for a in articles:
                article_html = requests.get(a.get_url()).text
                articleText = htmlParser.get_paragraphs(article_html)
                a.set_text(articleText)
                time.sleep(3)

            with article_list_lock:
                articleList.extend(articles) 


if __name__ == "__main__":
    #setting the number of threads
    THREAD_COUNT = 6


    #retreiving urls from text file        
    with open("url.txt") as f:
        rss_page_urls = f.read().split("\n")
        rss_page_urls = [x.strip() for x in rss_page_urls if len(x) > 0]
 
    # a list with all of the threads for joining them later on
    article_list_lock = threading.Lock()
    articleList = []


    url_queue_lock = threading.Lock()
    url_queue = Queue(len(rss_page_urls))

    #filling queue with urls from file
    for i in rss_page_urls:
        url_queue.put(i)
 
    # this will hold all of the contents taken from the articles
 
    getter_threads = [] 
    # starting threads
    for i in range(THREAD_COUNT):
        thread = downloadThread()
        thread.start()
        getter_threads.append(thread)

    # waiting for thread to be finished
    for name in getter_threads:
        name.join() 

    headlines = ""
    article_text = "" 
    for i in articleList:
        headlines = headlines + i.get_title() + "\n"

        title_block = "<item>\n<title>" + i.get_title() + "</title>" + "\n"
        content_block = "<article>" + i.get_text() + "\n</article>\n</item>\n"
        article_text = article_text + title_block + content_block

    
    #writing results to their respective files
    with open("headline.txt", "w") as h:
        h.write(headlines)
    with open("content.txt", "w") as c:
        c.write(article_text)



