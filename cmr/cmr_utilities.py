#!/usr/bin/env python3

#use urlopen to obtain html from a url
from urllib.request import urlopen, urlretrieve
from urllib import error
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup

#define the location of the cambridgemusicreviews site
#the page auto-revelas more content, accessible using increasing
#page_numbers
def get_cmr_url(page_number):
    #set the url based on the page number given
    url="https://cambridgemusicreviews.net/page/"+str(page_number)
    #print(url)
    return url    

web_page = {"exists":False, "html":"undefined"}
#go to the music reviews page and extracts the
#important information we need to process further
def get_httpresponse(url):
    #print("url is "+url)

    returned_web_page = web_page()
    #go to the given url and obtain the html 
    try:
        html = urlopen(url)
        soup = _get_soup(html)
        returned_web_page.soup = soup

        #print(get_soup(html).prettify())
        #bt wraps failure in a helpful page - look for no anchors
        if soup.find("a") == None:
#        if 1+1!=2:
#        if "webaddresshelp" in get_soup(html).prettify():
            #print("opened page ok, found no anchors")
            returned_web_page.exists = False;
            returned_web_page.html = ""
        else:
            returned_web_page.exists = True;
            #print("opened page ok, extract content")
            #print("html is "+str(html))
            #print(get_soup(html).prettify())
            returned_web_page.html = html


    except error.HTTPError as err:
       if err.code == 404:
           #print("got 404")
           returned_web_page.exists = False;
           returned_web_page.html = ""
       else:
           #print("did not get 404")
           returned_web_page.exists = True;
           returned_web_page.html = ""
        
    return returned_web_page

#save html from a url to a local file
def save_html(url, destination_file):
    urlretrieve(url, destination_file)    

#obtain a BeautifulSoup object which can parse the html
def _get_soup(html):

    #set up a beautifulsoup object to parse the html
    soup = BeautifulSoup(html, "lxml")

    #check the soup got the expected text
    #print(soup.prettify())

    return soup;

class web_page:
    exists = False
    html = ""
    soup = None

class CMR_Index_Categories:
    extra = "Extras"
    single_ep = "Singles and EPs"
    album = "Album reviews"
    live = "Live Reviews"
    undefined = "Undefined"
    

class CMR_Article:
    title = ""      # e.g. "ABC, Parker’s Piece, Cambridge, 7 July\xa02017"
    url = ""        # e.g. "https://cambridgemusicreviews.net/2017/07/09/abc-parkers-piece-cambridge-7-july-2017/"
    index_text = "" # e.g. "ABC"
    category = CMR_Index_Categories.undefined # e.g. CMR_Index_Categories.live
    
    def print_article_details(article):
            print("title      is :\""+article.title+"\"")
            print("url        is :\""+article.url+"\"")
            print("index_text is :\""+article.index_text+"\"")
            print("category   is :\""+article.category+"\"")


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
    #print(result);
    return result;
    
def sort_articles(articles):
    articles.sort(key = sort_key)

    