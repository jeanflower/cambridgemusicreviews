#!/usr/bin/env python3

import unittest

from cmr.cmr_utilities import CMR_Index_Categories
from cmr.cmr_get_articles_from_webpage import get_index_anchors

from bs4 import BeautifulSoup

from os import path

class Test_get_httpresponse(unittest.TestCase):

    def test_get_index_anchors(self):

        print("test_get_entry_titles...")
        #For testing, use html file stored in this codebase
        test_file = path.join(path.dirname(__file__), \
           'captured_pages/page_text_1.html')
        html = open(test_file)

        #------- GET DATA out of the web page of interest
        soup = BeautifulSoup(html, "lxml")

        #Use a sequence of calls to get the anchors out of each div
        articles = get_index_anchors(soup, "cmr-extras", CMR_Index_Categories.extra)
        articles = articles + get_index_anchors(soup, "cmr-singles", CMR_Index_Categories.single_ep)
        articles = articles + get_index_anchors(soup, "cmr-albums", CMR_Index_Categories.album)
        articles = articles + get_index_anchors(soup, "cmr-live", CMR_Index_Categories.live)

        #report back
        
        self.assertEqual(len(articles), 134);
        for i in range(0, 5):
            self.assertEqual(articles[i].category, CMR_Index_Categories.extra)
        for i in range(5, 22):
            self.assertEqual(articles[i].category, CMR_Index_Categories.single_ep)
        for i in range(22, 55):
            self.assertEqual(articles[i].category, CMR_Index_Categories.album)
        for i in range(55, 134):
            self.assertEqual(articles[i].category, CMR_Index_Categories.live)
        
        self.assertEqual(articles[0].title, "")
        self.assertEqual(articles[0].url, "https://cambridgemusicreviews.net/2015/12/23/12-highlights-from-2015-a-sampler-of-the-year/")
        self.assertEqual(articles[0].index_text, "12 Highlights from 2015")
        
#        print("articles found:")
#        article_number = 0
#        for article in articles:
#            article_number = article_number + 1
#            print("--------- article number "+str(article_number)+" "+article.index_text)
#        #    article.print_article_details();
#        print("done")

        html.close()