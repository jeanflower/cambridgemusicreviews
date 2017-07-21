#!/usr/bin/env python3

from cmr.cmr_utilities import get_cmr_url, get_httpresponse, get_soup
from cmr.cmr_get_articles_from_webpage import get_entry_titles 

#------- LOCATE a web page of interest

page_number = 1
#get url from cmr wordpress site
url = get_cmr_url(page_number)
html = get_httpresponse(url)

#------- GET DATA out of the web page of interest
soup = get_soup(html)

#simple test for getting articles out of the web page
#print("------ page 1 entry_title headings")
articles = get_entry_titles(soup)

#------- DO SOMETHING with the data
#print it out

print("articles found:")
article_number = 0
for article in articles:
    article_number = article_number + 1
    print("--------- article number "+str(article_number)+" -------------")
    article.print_article_details();
print("done")