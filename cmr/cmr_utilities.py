#!/usr/bin/env python3

from enum import IntEnum
#use urlopen to obtain html from a url
from urllib.request import urlopen, urlretrieve
from urllib import error
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup
from os import path

#define the location of the cambridgemusicreviews site
#the page auto-revelas more content, accessible using increasing
#page_numbers
def _get_cmr_url(page_number):
    #set the url based on the page number given
    url="https://cambridgemusicreviews.net/page/"+str(page_number)
    #print(url)
    return url

#go to the music reviews page and extracts the
#important information we need to process further
def _get_httpresponse(url):
    #print("url is "+url)

    returned_web_page = web_page()
    returned_web_page.exists = False
    returned_web_page.html = ""
    #go to the given url and obtain the html
    try:
        html = urlopen(url)  # nosec ; we know the url is made locally
        soup = _get_soup(html)
        returned_web_page.soup = soup

        #print(_get_soup(html).prettify())
        #bt wraps failure in a helpful page - look for no anchors
        if not soup.find("a") == None:
#        if not "webaddresshelp" in _get_soup(html).prettify():
            #print("opened page ok, found no anchors")
            returned_web_page.exists = True
            #print("opened page ok, extract content")
            #print("html is "+str(html))
            #print(_get_soup(html).prettify())
            returned_web_page.html = html


    except error.HTTPError as err:
       if not err.code == 404:
           #print("did not get 404")
           returned_web_page.exists = True
           returned_web_page.html = ""

    return returned_web_page

def get_cmr_page(page_number, local):
    if local:
        local_file = path.join(path.dirname(__file__), \
                     'captured_pages/page_text_1.html')
        html = open(local_file)
        #print("got web page "+str(web_page))

        returned_web_page = web_page()
        returned_web_page.exists = True
        returned_web_page.html = html
        returned_web_page.soup = _get_soup(html)
    
        html.close()
        return returned_web_page
    else:
        return _get_httpresponse(_get_cmr_url(page_number))

def save_cmr_page(page_number, destination_file):
     return _save_html(_get_cmr_url(page_number), destination_file)

#save html from a url to a local file
def _save_html(url, destination_file):
    try:
        urlretrieve(url, destination_file)  # nosec ; we know the url is made locally
        #print("no error")
        return True
    except error.HTTPError:
        #print("got error")
        return False

#obtain a BeautifulSoup object which can parse the html
def _get_soup(html):

    #set up a beautifulsoup object to parse the html
    soup = BeautifulSoup(html, "lxml")

    #check the soup got the expected text
    #print(soup.prettify())

    return soup

class web_page:
    exists = False
    html = ""
    soup = None

class CMR_Index_Categories(IntEnum):
    extra = 0     #"Extras"
    single_ep = 1 #"Singles and EPs"
    album = 2     #"Album reviews"
    live = 3      #"Live Reviews"
    undefined = 4 #"Undefined"

index_category_strings = ["Extras", "Singles and EPs", "Album reviews", 
                          "Live Reviews", "Undefined"]    

class CMR_Index_Status(IntEnum):
    from_html_index = 0 #"Derived from existing HTML index"
    from_code = 1       #"Guessed using code"
    from_enduser = 2    #"Set or confirmed by enduser"
    undefined = 3       #"Undefined"

class CMR_Article:
    title = ""      # e.g. "ABC, Parker’s Piece, Cambridge, 7 July\xa02017"
    url = ""        # e.g. "https://cambridgemusicreviews.net/2017/07/09/abc-parkers-piece-cambridge-7-july-2017/"
    index_text = "" # e.g. "ABC"
    category = CMR_Index_Categories.undefined # e.g. CMR_Index_Categories.live
    index_status = CMR_Index_Status.undefined

    def print_article_details(article):
            print("title      is :\""+article.title+"\"")
            print("url        is :\""+article.url+"\"")
            print("index_text is :\""+article.index_text+"\"")
            print("category   is :\""+index_category_strings[article.category]+"\"")


def sort_key(article):
    result= ""
    if article.category == CMR_Index_Categories.extra:
        result+="0 "
    elif article.category == CMR_Index_Categories.single_ep:
        result+="1 "
    elif article.category == CMR_Index_Categories.album:
        result+="2 "
    elif article.category == CMR_Index_Categories.live:
        result+="3 "
    else:
        result+="4 "
    if article.index_text[:3]=="The":
        result += article.index_text[4:].strip()
    else:
        result += article.index_text.strip()
    #print(result)
    return result

def sort_articles(articles):
    articles.sort(key = sort_key)

