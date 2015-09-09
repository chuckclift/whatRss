#!/usr/bin/python3

import time
import requests
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool as Pool
import sys
from random import shuffle
import argparse
import os.path
import feedparser

def get_html(url):
    try:
        return requests.get(url).text
    except:
        time.sleep(5)
        return requests.get(url).text
    return None

def get_feed(url):
    """Wraps the feedparser.parse function in error handling"""
    try:
        return feedparser.parse(url)
    except:
        print('error with: ', url)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('history', help='urls used in the past')
    parser.add_argument('-t','-threads', help='threads used to retreive articles')
    args = parser.parse_args()

    if os.path.isfile(args.history):
        with open(args.history) as h:
            used_urls = {a for a in h}
    else:
        used_urls = {}

    p = Pool(10)
   
    feed_docs = p.map(get_feed, (a for a in sys.stdin if len(a) > 5)) 

    entries = [a for b in feed_docs for a in b.entries]
    urls = [a.link for a in entries if not a.link in used_urls]

    with open(args.history, 'a') as hist:
        for u in urls:
            hist.write(u + '\n')


    html_docs = p.map(get_html, urls)

    for doc in html_docs:
        soup = BeautifulSoup(doc, "lxml")
        paragraphs = [paragraph.string for paragraph in soup.find_all('p')]
        paragraphs = filter(None, paragraphs)
        article = ' '.join(paragraphs)
        article = ' '.join(article.split())
        print(article)     


if __name__ == "__main__":
    main()
