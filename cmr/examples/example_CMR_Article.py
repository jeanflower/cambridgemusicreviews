#!/usr/bin/env python3

from cmr.cmr_utilities import CMR_Article, CMR_Index_Categories

#Create a CMR_Article object
print("------- create an article with no data in it")
my_article = CMR_Article()

# print out its contents
my_article.print_article_details()

# fill in some details
print("------- set a title for the article")
my_article.title = "Ed Sheeran, Wembley Stadium, July 1st 2017"

# print out its contents
my_article.print_article_details()

# fill in more details
print("------- set other data for the article")
my_article.url = "http://made_up_address.html"
my_article.index_text = "Ed Sheeran"
my_article.category = CMR_Index_Categories.live

# print out its contents
my_article.print_article_details()

# change in some details
print("------- set a title for the article")
my_article.title = "Ed Sheeran, Wembley Stadium, August 11th 2017"

# print out its contents
my_article.print_article_details()

