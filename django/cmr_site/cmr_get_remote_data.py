#use urlopen to obtain html from a url
from urllib.request import urlopen, urlretrieve
from urllib import error
from cmr_utilities import get_soup
from indexer.models import Article, CMR_Index_Status
from cmr_get_articles_from_webpage import make_url_map_from_local_html_page

import requests
import html
import re

#define the location of the cambridgemusicreviews site
#the page auto-revelas more content, accessible using increasing
#page_numbers
def _get_cmr_url(page_number):
    #set the url based on the page number given
    url = "https://cambridgemusicreviews.net/page/"+str(page_number)
    #print(url)
    return url


#save html from a url to a local file
def _save_html(url, destination_file):
    try:
        urlretrieve(url, destination_file)  # nosec ; we know the url is made locally
        #print("no error")
        return True
    except error.URLError:
        #print("got URL error")
        return False
    except error.HTTPError:
        #print("got HTTP error")
        return False
        
# Save a CMR page obtained from WordPress as a local html file.
def save_cmr_page(page_number, destination_file):
    return _save_html(_get_cmr_url(page_number), destination_file)

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
        soup = get_soup(html)
        returned_web_page.soup = soup

        #print(get_soup(html).prettify())
        #bt wraps failure in a helpful page - look for no anchors
        if not soup.find("a") is None:
#        if not "webaddresshelp" in get_soup(html).prettify():
            #print("opened page ok, found no anchors")
            returned_web_page.exists = True
            #print("opened page ok, extract content")
            #print("html is "+str(html))
            #print(get_soup(html).prettify())
            returned_web_page.html = html


    except error.HTTPError as err:
        if not err.code == 404:
            #print("did not get 404")
            returned_web_page.exists = True
            returned_web_page.html = ""

    return returned_web_page

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

# From both articles and existing index, combined
def get_wp_articles():
    quick_test = False
#    print("get articles")
    articles = _get_all_cmr_articles_no_index(quick_test)
#    print("got articles")
    _add_existing_index_data(articles)
    return articles

# Given a set of found articles, look at the existing index
# and fill in known index_title and category information
def _add_existing_index_data(articles):

    url_map = make_url_map_from_local_html_page();
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

