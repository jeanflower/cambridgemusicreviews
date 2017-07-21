#!/usr/bin/env python3

from cmr_utilities import CMR_Index_Categories, CMR_Article


#DONE : obtain article data from web page articles
# see cmr_get_articles_from_webpage.py
# (prints out partly defined article data from web page)

#TODO : obtain article data from existing index in web page
# NB this will only be partly defined; no title, 
# but will have url, index title and category

#TODO : combine article data from web page (including existing index)
# note both indexes from web page and from index text will be incomplete
# but the url is shared data and lets us combine the two

#TODO : save article data
# write to a file, either a text file, or csv,m or some special python format

#TODO : load article data
# recover a list of CMR_Articles from a saved file

#TODO : write a utility to find gaps in article data and ask the user
# given a list of CMR_Articles, look for empty strings or undefined
# categories, ask the user to help, fill in the missing data
# offer to save when done

#TODO : write a utility to let a user edit data in the article data
# given a list of CMR_Articles, let the user make edits and save

#TODO : create index html from article data
# given a list of CMR_Articles, make a file index.html which can
# be viewed independently or
# pasted into the WordPress widget


