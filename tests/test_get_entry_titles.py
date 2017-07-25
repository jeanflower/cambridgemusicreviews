#!/usr/bin/env python3

import unittest

from cmr.cmr_utilities import web_page
from cmr.cmr_get_articles_from_webpage import get_entry_titles
from bs4 import BeautifulSoup

from os import path


class Test_get_entry_titles(unittest.TestCase):

    def test_get_entry_titles(self):
        print("test_get_entry_titles...")
        #For testing, use html file stored in this codebase
        test_file = path.join(path.dirname(__file__), \
           'captured_pages/page_text_1.html')
        html = open(test_file)

        #------- GET DATA out of the web page of interest
        soup = BeautifulSoup(html, "lxml")

        this_web_page = web_page()
        this_web_page.exists = True
        this_web_page.html = html
        this_web_page.soup = soup

        #simple test for getting articles out of the web page

        #print("------ page 1 entry_title headings")
        articles = get_entry_titles(this_web_page)

        # the test doc has 7 articles
        self.assertEqual(len(articles), 7)

        #assert the contents of the last article
        #print(articles[6].title)
        self.assertEqual(articles[6].title,\
            "The Scissors, Corner House, Cambridge, 1 April\xa02017");
        self.assertEqual(articles[6].url,\
            "https://cambridgemusicreviews.net/2017/04/05/"+\
            "the-scissors-corner-house-cambridge-1-april-2017/");
        self.assertEqual(articles[6].index_text, "");
        self.assertEqual(articles[6].category, "Undefined");

        html.close()

if __name__ == '__main__':
    unittest.main()
