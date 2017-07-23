#!/usr/bin/env python3

import unittest

from cmr.cmr_utilities import CMR_Article, \
                              CMR_Index_Categories, \
                              sort_articles

class Test_CMR_Article(unittest.TestCase):

    def test_build_article(self):
        print("test_build_article...")
        
        article = CMR_Article()
        
        example_title = "ABC, Parker’s Piece, 7 July 2017"
        article.title = example_title
        self.assertEqual(article.title,example_title)
        #self.assertEqual(article.title,"hello") #uncomment to see test failure
        
        example_url = "https://cambridgemusicreviews.net/2017/07/09/"\
             +"abc-parkers-piece-cambridge-7-july-2017/"
        article.url = example_url
        self.assertEqual(article.url, example_url)
        
    def test_sort_articles(self):
        sample_article_0 = CMR_Article()
        sample_article_0.title = "ABC, Parker’s Piece, 7 July 2017"
        sample_article_0.url = "http://example_url_0.com"
        
        sample_article_1 = CMR_Article()
        sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
        sample_article_1.url = "http://example_url_1.com"
        sample_article_1.index_text = "Lee Hull, 4th June 2017"
        sample_article_1.category = CMR_Index_Categories.live
        
        sample_article_2 = CMR_Article()
        sample_article_2.title = "z"
        sample_article_2.url = "http://example_url_0.com"
        sample_article_2.index_text = "z"
        sample_article_2.category = CMR_Index_Categories.extra
        
        sample_article_3 = CMR_Article()
        sample_article_3.title = "z"
        sample_article_3.url = "http://example_url_0.com"
        sample_article_3.index_text = "w"
        sample_article_3.category = CMR_Index_Categories.extra
        
        
        articles = [sample_article_0, sample_article_1, 
                    sample_article_2, sample_article_3]
        
        sort_articles(articles)
            
        self.assertEqual(articles[0].title,'z')
        self.assertEqual(articles[0].index_text,'w')
        self.assertEqual(articles[1].title,'z')
        self.assertEqual(articles[1].index_text,'z')
        self.assertEqual(articles[2].title,"Lee Hull, Corner House, Cambridge, 4 June 2017")
        self.assertEqual(articles[3].title,"ABC, Parker’s Piece, 7 July 2017")

if __name__ == '__main__':
    unittest.main()
