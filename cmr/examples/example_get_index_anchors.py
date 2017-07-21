#!/usr/bin/env python3

from cmr.cmr_utilities import get_cmr_url, get_httpresponse, get_soup
from cmr.cmr_utilities import CMR_Index_Categories
from cmr.cmr_get_articles_from_webpage import get_index_anchors

#------- LOCATE a web page of interest

page_number = 1
#get url from cmr wordpress site
url = get_cmr_url(page_number)
html = get_httpresponse(url)

#------- GET DATA out of the web page of interest
soup = get_soup(html)
#Use a sequence of calls to get the anchors out of each div
articles = get_index_anchors(soup, "cmr-extras", CMR_Index_Categories.extra)
articles = articles + get_index_anchors(soup, "cmr-singles", CMR_Index_Categories.single_ep)
articles = articles + get_index_anchors(soup, "cmr-albums", CMR_Index_Categories.album)
articles = articles + get_index_anchors(soup, "cmr-live", CMR_Index_Categories.live)

#report back
print("articles found:")
article_number = 0
for article in articles:
    article_number = article_number + 1
    print("--------- article number "+str(article_number)+" "+article.category)
#    article.print_article_details();
print("done")