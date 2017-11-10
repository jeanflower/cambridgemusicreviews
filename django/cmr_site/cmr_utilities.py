#!/usr/bin/env python3

#use urlopen to obtain html from a url
from urllib.request import urlopen, urlretrieve
from urllib import error
from os import path
#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup

from indexer.models import CMR_Index_Categories

#define the location of the cambridgemusicreviews site
#the page auto-revelas more content, accessible using increasing
#page_numbers
def _get_cmr_url(page_number):
    #set the url based on the page number given
    url = "https://cambridgemusicreviews.net/page/"+str(page_number)
    #print(url)
    return url

#go to the music reviews page and extracts the
#important information we need to process further
def _get_httpresponse(url):
    #print("url is "+url)

    returned_web_page = Web_Page()
    returned_web_page.exists = False
    returned_web_page.html = ""
    #go to the given url and obtain the html
    try:
        html = urlopen(url)  # nosec ; we know the url is made locally
        soup = _get_soup(html)
        returned_web_page.soup = soup

        #print(_get_soup(html).prettify())
        #bt wraps failure in a helpful page - look for no anchors
        if not soup.find("a") is None:
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

# Get an HttpResponse for the CMR page with given number.
# NB wordpress serves up CMR articles in batches / pages.
# Optionally, get the data from a local file (quicker for debugging work).
def get_local_cmr_page():
    local_file = path.join(path.dirname(__file__), \
                 'captured_pages/page_text_1.html')
    html = open(local_file)

    returned_web_page = Web_Page()
    returned_web_page.exists = True
    returned_web_page.html = html
    returned_web_page.soup = _get_soup(html)

    html.close()
    return returned_web_page

# Save a CMR page obtained from WordPress as a local html file.
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

# A data structure which represents the result from an attempt to get
# a web page; it can say the page didn't exist, or it can have HTML,
# and it can have a soup representation too.
class Web_Page:
    exists = False
    html = ""
    soup = None

def sort_key(article):
    result = ""
    if article.category == CMR_Index_Categories.extra:
        result += "0 "
    elif article.category == CMR_Index_Categories.single_ep:
        result += "1 "
    elif article.category == CMR_Index_Categories.album:
        result += "2 "
    elif article.category == CMR_Index_Categories.live:
        result += "3 "
    else:
        result += "4 "
    if article.index_text[:3] == "The":
        result += article.index_text[4:].strip()
    else:
        result += article.index_text.strip()
    #print(result)
    return result

def sort_articles(articles):
    articles.sort(key=sort_key)
