#!/usr/bin/env python3

#use urlopen to obtain html from a url
from urllib.request import urlopen, urlretrieve
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

#go to the music reviews page and extracts the
#important information we need to process further
def get_httpresponse(url):
    #go to the given url and obtain the html 
    html = urlopen(url)
    #print(html)
    return html

#save html from a url to a local file
def save_html(url, destination_file):
    urlretrieve(url, destination_file)    

#obtain a BeautifulSoup object which can parse the html
def get_soup(html):

    #set up a beautifulsoup object to parse the html
    soup = BeautifulSoup(html, "lxml")

    #check the soup got the expected text
    #print(soup.prettify())

    return soup;


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
    