#!/usr/bin/python3
import re

def get_urls(html):
    regex = "<a.*?>"
    anchor_list = re.findall(regex, html)
    html_urls = []
    
    # getting the urls from the html document    
                              
    for a in anchor_list:
        url_beginning = a.find("href=") + 6
 
        if url_beginning is not -1:
            _ = a[url_beginning:-1]
            url_end = _.find("\"")
            url = _[0:url_end]
            html_urls.append(url)

    # filtering out the "#" values
    html_urls = [x for x in html_urls if x.strip() is not "#"]


    # filtering out all values that don't start with "http" or
    # "/" so that only values like these remain
    #        "https://www.whatever.com
    #        "/relative/link/

    for i in html_urls:
        # filtering out all values that don't start with 
        # "http" or "/"
        http_at_start = i.startswith("http")
        slash_at_start = i.startswith("/")

       
        if not http_at_start and not slash_at_start:
            html_urls.remove(i) 

    return html_urls 
        
    
def get_paragraphs(html):    
    # getting everything between the p tags
    p_tags = re.findall(r'<p>.*</p>', html)
    
    # filtering out the tags left inside the pargraphs
    p_tags = [re.sub(r'<(.*?)>','', x) for x in p_tags]

    paragraph_text = "\n".join(p_tags)
    return paragraph_text
 

    
if __name__ == "__main__":
    with open("example.html", encoding="utf-8") as f:
        sampleHtml = f.read()
    print(get_paragraphs(sampleHtml)) 
