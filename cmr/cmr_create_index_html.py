#!/usr/bin/env python3

from cmr.cmr_utilities import CMR_Article, CMR_Index_Categories

def get_index_html(articles):
    print("Error : html output not yet implemented")
    #TODO : write some HTML here, at the moment it generates other text
    html = "start of html here\n"
    for article in articles:        
        html = html + "\nsome more html\n"
        html = html + article.index_text
        html = html + "\neven more html\n"
        html = html + article.url
        html = html + "\nyet more html\n"
        
    return html

def save_index_html(articles, filename):
    get_index_html(articles)
    print("Error : save not yet implemented")
    #TODO : save to a file called filename
    

#Set up an example of a couple of articles we might want to convert into
#an index
sample_article_0 = CMR_Article()
sample_article_0.title = "ABC, Parker’s Piece, 7 July 2017"
sample_article_0.url = "http://example_url_0.com"
sample_article_0.index_text = "ABC, 7th July 2017"
sample_article_0.category = CMR_Index_Categories.album

sample_article_1 = CMR_Article()
sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
sample_article_1.url = "http://example_url_1.com"
sample_article_1.index_text = "Lee Hull, 4th June 2017"
sample_article_1.category = CMR_Index_Categories.live

articles = [sample_article_0, sample_article_1]

print(get_index_html(articles))

#save_index_html(articles, "test.html")
