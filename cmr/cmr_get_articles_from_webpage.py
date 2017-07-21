#!/usr/bin/env python3

from cmr.cmr_utilities import get_cmr_url, get_httpresponse, get_soup
from cmr.cmr_utilities import CMR_Article, CMR_Index_Categories


#Choose the headings which have class = entry-title
def get_entry_titles(soup):    
    #set up an empty list to hold data for each link
    articles_found = []

    #the headings we're interested in all have class=entry-title
    #ask soup for a list of such headings
    myH1s = soup.findAll("h1", { "class" : "entry-title" })
    
    #iterate over these headings compiling data into result_data
    for h1 in myH1s: 
        #for each one get the text the human sees and the link url
        this_title = h1.find('a').contents[0]
        this_url = h1.find('a')["href"]

        # build a CMR_Article
        this_article = CMR_Article()
        this_article.title = this_title
        this_article.url = this_url
        articles_found.append(this_article)
        
    #pass the results back to the calling code    
    return articles_found

#############

#Choose the index anchors which have given tag, save Article with given category
def get_index_anchors(soup, tag, category):    
    #set up an empty list to hold data for each link
    articles_found = []

    #the headings we're interested in all have class = given tag
    #ask soup for a list of such headings
    my_div = soup.find("div", { "class" : tag })
    anchors = my_div.findAll('a')
    
    #iterate over these anchors compiling data into result_data
    for anchor in anchors: 
        #for each one get the text the human sees and the link url
        this_index_text = str(anchor.contents[0])
        this_url = str(anchor["href"])

        # build a CMR_Article
        this_article = CMR_Article()
        this_article.index_text = this_index_text
        this_article.url = this_url
        this_article.category = category
        articles_found.append(this_article)
        
    #pass the results back to the calling code    
    return articles_found



