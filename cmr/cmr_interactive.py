#!/usr/bin/env python3

from cmr.cmr_utilities import  CMR_Article, CMR_Index_Categories

def get_missing_index_text_interactive(article):
    # TODO : ask the user to input some text and use their response            
    print("missing index text")
    print("article title was \""+ article.title+"\"")
    return "junk - get_missing_index_text not yet written"

def get_missing_category_interactive(article):
    # TODO : ask the user to input a category and use their response
    print("missing category")
    print("article title was \""+ article.title+"\"")
    print("Error : get_missing_category not yet written")
    return CMR_Index_Categories.undefined

# Find out whether articles have missing index_text or category
# and ask the user to provide the information.
# Store result back in articles
def fill_in_missing_data(articles, 
                         get_missing_index_text, 
                         get_missing_category):
    for article in articles:
        # an article which already has index_text and a category is complete
        has_index_text = len(article.index_text) > 0
        has_category = article.category != CMR_Index_Categories.undefined
        if has_index_text and has_category:
            continue

        if not has_index_text:
            article.index_text = get_missing_index_text(article)
        
        if not has_category:
            article.category = get_missing_category(article)

