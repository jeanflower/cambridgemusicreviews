#!/usr/bin/env python3

from cmr.cmr_utilities import \
    CMR_Article, get_cmr_url, get_httpresponse, CMR_Index_Categories

#  Given a page with articles,
#  obtain index-relevant data from the articles.
#  Data comes back as (partially complete)
#  CMR_Article objects; we'll know the title and url.

#  Given a page with an existing index,
#  obtain the data from the index.
#  Expect to find categoriseddata tagged by
#  "cmr-extras", "cmr-singles", "cmr-albums" and "cmr-live".
#  Data comes back as (partially complete)
#  CMR_Article objects; we'll know the index text, url and category.

#Choose the headings which have class = entry-title
def get_entry_titles(web_page):
    soup = web_page.soup

    #set up an empty list to hold data for each link
    articles_found = []

    if soup == None:
        print("error : no soup?")
        return articles_found

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
        this_article.title = str(this_title)
        this_article.url = this_url
        articles_found.append(this_article)

    #pass the results back to the calling code
    return articles_found

# Iterate over all cmr articles extracting article data until
# we get to a page that doesn't exist.
# Return a list of all articles found.
def _get_all_cmr_articles(quick_test):

    articles_found = []

    max_page_number = 100; #current max is 20
    if quick_test:
        max_page_number = 2

    for page_number in range(1, max_page_number):
        web_page = get_httpresponse(get_cmr_url(page_number))
        if not(web_page.exists):
            break;
        articles_found = articles_found + get_entry_titles(web_page)

    return articles_found;

def get_all_cmr_articles():
    return _get_all_cmr_articles(False)

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

def _extend_url_map(soup, div_string, category, url_map):
    articles = get_index_anchors(soup, div_string, category)
    for article in articles:
        url_map[article.url] = article

# Given a set of found articles, look at the existing index
# and fill in known index_title and category information
def _add_existing_index_data(articles):
    # all indexes should be the same, look at page 1
    web_page = get_httpresponse(get_cmr_url(1))
    soup = web_page.soup

    # Use URL as key in a map
    url_map = dict()
    _extend_url_map(soup, "cmr-extras", CMR_Index_Categories.extra, url_map)
    _extend_url_map(soup, "cmr-singles", CMR_Index_Categories.single_ep, url_map)
    _extend_url_map(soup, "cmr-albums", CMR_Index_Categories.album, url_map)
    _extend_url_map(soup, "cmr-live", CMR_Index_Categories.live, url_map)

    for article in articles:
        map_entry = url_map.get(article.url)
        if map_entry == None:
            continue
        article.index_text = map_entry.index_text
        article.category = map_entry.category

# From both articles and existing index, combined
def _get_all_cmr_data(quick_test):
    articles = _get_all_cmr_articles(quick_test)
    _add_existing_index_data(articles)
    return articles

def get_all_cmr_data_quick_test():
    return _get_all_cmr_data(True)

def get_all_cmr_data():
    return _get_all_cmr_data(False)
