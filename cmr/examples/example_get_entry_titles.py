#!/usr/bin/env python3

from cmr.cmr_utilities import get_cmr_url, get_httpresponse
from cmr.cmr_get_articles_from_webpage import get_entry_titles 

#------- LOCATE a web page of interest

page_number = 1
#get url from cmr wordpress site
url = get_cmr_url(page_number)
this_web_page = get_httpresponse(url)
    
if this_web_page.exists:
    #------- GET DATA out of the web page of interest

    #simple test for getting articles out of the web page
    #print("------ page 1 entry_title headings")
    articles = get_entry_titles(this_web_page)
    
    #------- DO SOMETHING with the data
    #print it out
    
    print("articles found:")
    article_number = 0
    for article in articles:
        article_number = article_number + 1
        print("--------- article number "+str(article_number)+" -------------")
        article.print_article_details();
    print("done")
else:
    print("no such page")
    