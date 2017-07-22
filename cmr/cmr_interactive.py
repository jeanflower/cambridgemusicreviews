#!/usr/bin/env python3

from cmr.cmr_utilities import CMR_Article, CMR_Index_Categories

def get_missing_index_text_interactive(article):
    # TODO : ask the user to input some text and use their response     
    print("missing index text")
    
    print("current article is\n")
    article.print_article_details()
    response = input("please type in text to use for index link (e.g. : Lee Hull, 4th June 2017): ")
    return response

    proposed_data = CMR_Article()
    proposed_data.title = article.title
    proposed_data.url = article.url
    proposed_data.index_text = response
    proposed_data.category = article.category

    print("proposed article : ")
    proposed_data.print_article_details()
    ok = input("use this new data? (y/n): ")
    if ok=='y':
        return response
    else:
        return ""

def get_missing_category_interactive(article):
    # TODO : ask the user to input a category and use their response
    print("missing category")
    print("article title was \""+ article.title+"\"")
    print("Possible categories are ")
    print("  Extras          (e)")
    print("  Singles and EPs (s)")
    print("  Album reviews   (a)")
    print("  Live Reviews    (l)")    
    response = input("please type in a category (e/s/a/l): ")
    cat = CMR_Index_Categories.undefined
    if response == 'e' :
        cat = CMR_Index_Categories.extra
    elif response == 's' :
        cat = CMR_Index_Categories.single_ep
    elif response == 'a' :
        cat = CMR_Index_Categories.album
    elif response == 'l' :
        cat = CMR_Index_Categories.live

    proposed_data = CMR_Article()
    proposed_data.title = article.title
    proposed_data.url = article.url
    proposed_data.index_text = article.index_text
    proposed_data.category = cat
    
    print("proposed article : ")
    proposed_data.print_article_details()
    ok = input("use this new data? (y/n): ")
    if ok=='y':
        return cat
    else:
        return ""

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

