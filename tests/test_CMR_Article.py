#!/usr/bin/env python3

import unittest

from cmr.cmr_utilities import CMR_Article

class Test_CMR_Article(unittest.TestCase):

    def test_build_article(self):
        article = CMR_Article()
        
        example_title = "ABC, Parker’s Piece, 7 July 2017"
        article.title = example_title
        self.assertEqual(article.title,example_title)
        #self.assertEqual(article.title,"hello") #uncomment to see test failure
        
        example_url = "https://cambridgemusicreviews.net/2017/07/09/"\
             +"abc-parkers-piece-cambridge-7-july-2017/"
        article.url = example_url
        self.assertEqual(article.url, example_url)


if __name__ == '__main__':
    unittest.main()
