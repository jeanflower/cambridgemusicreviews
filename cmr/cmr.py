#!/usr/bin/env python3


#DONE : obtain titles and urls from articles on a specified web page
# gets title, url for each
#
# cmr_get_articles_from_webpage.get_entry_titles
# Test_get_entry_titles
# usage example:  example_get_entry_titles.py

#DONE : obtain article data from existing index in a specified web page
# gets url, index title and category
#
# get_index_anchors
# tested only via get_all_cmr_data
# usage example: example_get_index_anchors.py

#TODO? : make CMR_Index_Categories into an extensible list
# it's tightly bound to the html that's written and stored in the HTML
# index.  Do we want to easily add or change the categories?

#DONE : combine article data from web page (including existing index)
# note both indexes from web page and from index text will be incomplete
# but the url is shared data and lets us combine the two
# 
# get_all_cmr_data
# Test_get_all_cmr_data
# usage example: example_get_all_cmr_data.py

#DONE : write a function to find gaps in article data and fills them in
# given a list of CMR_Articles, look for empty strings or undefined
# categories, gets help, fill in the missing data
#
# fill_in_missing_data 

#TODO : get missing data from user
# Given an article with missing index_text or category,
# get help from the user to determine the right string/category
# and fill it in.
# see cmr_interactive.py

#TODO : create index html from article data
# given a list of CMR_Articles, make a file index.html which can
# be viewed independently or
# pasted into the WordPress widget
#
# see cmr_create_index.py

#TODO : write a utility to let a user edit data in the article data
# given a list of CMR_Articles, let the user make edits



