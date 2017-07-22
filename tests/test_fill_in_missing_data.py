#!/usr/bin/env python3

import unittest

from cmr.cmr_utilities import CMR_Article, CMR_Index_Categories
from cmr.cmr_interactive import fill_in_missing_data

def get_missing_index_text_test(article):
    return article.title[:5] # for testing, use first 5 characters of title

def get_missing_category_test(article):
    return CMR_Index_Categories.album

class Test_fill_in_missing_data(unittest.TestCase):

    
    def test_fill_in_missing_data(self):
        sample_article_0 = CMR_Article()
        sample_article_0.title = "ABC, Parker’s Piece, 7 July 2017"
        sample_article_0.url = "http://example_url_0.com"
        
        sample_article_1 = CMR_Article()
        sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
        sample_article_1.url = "http://example_url_1.com"
        sample_article_1.index_text = "Lee Hull, 4th June 2017"
        sample_article_1.category = CMR_Index_Categories.live
        
        articles = [sample_article_0, sample_article_1]
                
        fill_in_missing_data(articles,
                             get_missing_index_text_test, 
                             get_missing_category_test)
            
        self.assertEqual(articles[0].title, "ABC, Parker’s Piece, 7 July 2017")
        self.assertEqual(articles[0].url, "http://example_url_0.com")
        self.assertEqual(articles[0].index_text, "ABC, 7th July")
        self.assertEqual(articles[0].category, CMR_Index_Categories.live)
        
        self.assertEqual(articles[1].title, "Lee Hull, Corner House, Cambridge, 4 June 2017")
        self.assertEqual(articles[1].url, "http://example_url_1.com")
        self.assertEqual(articles[1].index_text, "Lee Hull, 4th June 2017")
        self.assertEqual(articles[1].category, CMR_Index_Categories.live
        )

if __name__ == '__main__':
    unittest.main()



