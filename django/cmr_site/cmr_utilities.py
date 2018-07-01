#!/usr/bin/env python3

#use beautifulsoup library to parse the html
from bs4 import BeautifulSoup

from indexer.models import CMR_Index_Categories


#obtain a BeautifulSoup object which can parse the html
def get_soup(html):

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
    
IGNORE_START_STRINGS = ["The ", "'", "\"", "“", "‘"]

def sort_key(article):

    result = ""

# It's not obvious how this ordering of categories affects things...
# or whether we could reuse the enum value
    if article.category == CMR_Index_Categories.live:
        result += "0 "
    elif article.category == CMR_Index_Categories.album:
        result += "1 "
    elif article.category == CMR_Index_Categories.single_ep:
        result += "2 "
    elif article.category == CMR_Index_Categories.extra:
        result += "3 "
    else:
        result += "4 "

    rest_of_result = article.index_text
    for ignore_string in IGNORE_START_STRINGS:
        len_string = len(ignore_string)
        start_of_index = article.index_text[:len_string]
#        print("compare "+ignore_string+" and "+start_of_index)
        if start_of_index == ignore_string: # TODO find better way
#            print("found ignore-string "+ignore_string)
            rest_of_result = rest_of_result[(len_string):]
    result += rest_of_result.strip()
#    print(result)
    return result

def sort_articles(articles):
    articles.sort(key=sort_key)


