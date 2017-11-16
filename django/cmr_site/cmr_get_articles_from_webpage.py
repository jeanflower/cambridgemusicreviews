#!/usr/bin/env python3

from cmr_utilities import get_local_cmr_page

from indexer.models import Article,\
                           CMR_Index_Categories, CMR_Index_Status

import requests
import re
import html

#  Given the CMR with articles,
#  obtain index-relevant data from the articles.
#  Use the wordpress REST API.
#  Data comes back as (partially complete)
#  Article objects; we'll know the title and url.

def _get_all_cmr_articles_no_index(quick_test):
    #set up an empty list to hold data for each link
    articles_found = []

    # Wordpress serves up data one page at a time
    # Today we have 8 pages. Allow site to grow to 1000 pages.
    for page_number in range(1, 1000):
        url = "https://public-api.wordpress.com/rest/v1.1/sites/"\
             +"cambridgemusicreviews.net/posts"
             
        # influences the formatting of the results
        url+= "?context=\"display\""

        url+= "&page="+str(page_number)
        
        if quick_test:
            # ask for 4 results only
            url+= "&number=4"
        
        posts = []
        
        try:
            ret = requests.get(url)
            returned_code = ret.status_code
            #print("returned value is "+str(ret.status_code))
            
            if returned_code == 200:
                posts = ret.json()["posts"]
            else:
                print("error from REST API request")
                break
        
        except requests.exceptions.ConnectionError as err:
            print("no connection for REST API request")
            break
            
        if len(posts) == 0:
            break

        #print("got "+str(len(posts))+" posts")
        
        for post in posts:
            # build a CMR_Article
            this_article = Article()
            this_article.title = html.unescape(post["title"])
            this_article.url = post["URL"]
            this_article.tags = list(post["tags"].keys())
            this_article.index_status = CMR_Index_Status.undefined
            articles_found.append(this_article)

    #pass the results back to the calling code
    return articles_found

#  Given a page with an existing index,
#  obtain the data from the index.
#  Expect to find categorised data tagged by
#  "cmr-extras", "cmr-singles", "cmr-albums" and "cmr-live".
#  Data comes back as (partially complete)
#  CMR_Article objects; we'll know the index text, url and category.

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
        this_article = Article()
        this_article.index_text = this_index_text
        this_article.url = this_url
        this_article.category = category
        this_article.index_status = CMR_Index_Status.from_html_index
        articles_found.append(this_article)

    #pass the results back to the calling code
    return articles_found

def extend_url_map(soup, div_string, category, url_map):
    articles = get_index_anchors(soup, div_string, category)
    for article in articles:
        url_map[article.url] = article

def _report_unexpected_category(article):
    print("unexpected category!!!")
    print(article.title)
    print(article.url)
    print(str(article.tags))
    print(str(article.category))

# Given a set of found articles, look at the existing index
# and fill in known index_title and category information
def _add_existing_index_data(articles):
    # all indexes should be the same, look at page 1
    web_page = get_local_cmr_page()

    soup = web_page.soup

    # Use URL as key in a map
    url_map = dict()
    extend_url_map(soup, "cmr-extras", CMR_Index_Categories.extra, url_map)
    extend_url_map(soup, "cmr-singles", CMR_Index_Categories.single_ep, url_map)
    extend_url_map(soup, "cmr-albums", CMR_Index_Categories.album, url_map)
    extend_url_map(soup, "cmr-live", CMR_Index_Categories.live, url_map)

    #print(url_map)

    for article in articles:
        # we're treating the URL string as a unique key for each article
        # but sometimes they are http and sometimes https
        map_entry = url_map.get(article.url)
        if map_entry == None and "http:" in article.url:
            map_entry = url_map.get(re.sub("http:", "https:", article.url))
        if map_entry == None and "https:" in article.url:
            map_entry = url_map.get(re.sub("https:", "http:", article.url))
        if map_entry == None:
            #print("umatched url "+article.url)
            continue
        
        article.index_text = map_entry.index_text
        article.category = map_entry.category
        article.index_status = map_entry.index_status

# From both articles and existing index, combined
def _get_wp_articles(quick_test):
    articles = _get_all_cmr_articles_no_index(quick_test)
    _add_existing_index_data(articles)
    return articles

def get_all_cmr_data_quick_test():
    return _get_wp_articles(True)

def get_wp_articles():
    return _get_wp_articles(False)
