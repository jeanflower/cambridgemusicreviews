#!/usr/bin/env python3

#  Given a page with an existing index,
#  obtain the data from the index.
#  Expect to find categorised data tagged by
#  "cmr-extras", "cmr-singles", "cmr-albums" and "cmr-live".
#  Data comes back as (partially complete)
#  CMR_Article objects; we'll know the index text, url and category.

from os import path
from cmr_utilities import Web_Page, get_soup
from indexer.models import Article, CMR_Index_Status, html_tags, categories

import re

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
    returned_web_page.soup = get_soup(html)

    html.close()
    return returned_web_page



#Choose the index anchors which have given tag, save Article with given category
def _get_index_anchors(soup, category):
    #set up an empty list to hold data for each link
    articles_found = []

    #the headings we're interested in all have class = given tag
    #ask soup for a list of such headings
    tag = html_tags[category]
    my_div = soup.find("div", { "class" : tag })

    if my_div == None:
        return articles_found;
#    print(my_div)

    anchors = my_div.findAll('a')
#    anchors = my_div.findAll()

    #iterate over these anchors compiling data into result_data
    for anchor in anchors:
        #for each one get the text the human sees and the link url
        if len(anchor.contents) == 0:
#            print("unexpected anchor with no contents")
#            print(anchor)
            #stop processing this useless anchor
            continue
        this_index_text = str(anchor.contents[0])
        this_url = str(anchor["href"])

        # build a CMR_Article
        this_article = Article()
        this_article.index_text = this_index_text
        this_article.url = this_url
        this_article.category = category
        this_article.index_status = CMR_Index_Status.from_html_index
        articles_found.append(this_article)

    #pass the results back to the calling code
    return articles_found

def _extend_url_map(soup, category, url_map):
#    print("extending url map for "+html_tags[category])
    articles = _get_index_anchors(soup, category)
    for article in articles:
        url_map[article.url] = article

# The url_map has
# key = url of wordpress article
# value = corresponding Article object
# An html page can populate this map by interrogating the
# anchors of the html (beautiful-soup html parsing)
def make_url_map_from_local_html_page():
    # all indexes should be the same, look at page 1
    web_page = get_local_cmr_page()

    soup = web_page.soup

    # Use URL as key in a map
    url_map = dict()

    for section in categories:
        _extend_url_map(soup, section, url_map)

    return url_map

