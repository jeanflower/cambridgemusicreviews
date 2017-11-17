#!/usr/bin/env python3

import unittest

from indexer.models import Article, \
                           CMR_Index_Categories

from cmr_utilities import  sort_articles

class Test_Article(unittest.TestCase):

    def test_build_article(self):
        #print("test_build_article...")

        article = Article()

        example_title = "ABC, Parker’s Piece, 7 July 2017"
        article.title = example_title
        self.assertEqual(article.title,example_title)
        #self.assertEqual(article.title,"hello") #uncomment to see test failure

        example_url = "https://cambridgemusicreviews.net/2017/07/09/"\
             +"abc-parkers-piece-cambridge-7-july-2017/"
        article.url = example_url
        self.assertEqual(article.url, example_url)

    def test_sort_articles(self):
        sample_article_0 = Article()
        sample_article_0.title = "ABC, Parker’s Piece, 7 July 2017"
        sample_article_0.url = "http://example_url_0.com"
        sample_article_0.category = CMR_Index_Categories.live

        sample_article_1 = Article()
        sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
        sample_article_1.url = "http://example_url_1.com"
        sample_article_1.index_text = "Lee Hull, 4th June 2017"
        sample_article_1.category = CMR_Index_Categories.live

        sample_article_2 = Article()
        sample_article_2.title = "z"
        sample_article_2.url = "http://example_url_0.com"
        sample_article_2.index_text = "z"

        sample_article_3 = Article()
        sample_article_3.title = "z"
        sample_article_3.url = "http://example_url_0.com"
        sample_article_3.index_text = "w"
        sample_article_3.category = CMR_Index_Categories.extra

        sample_article_4 = Article()
        sample_article_4.title = "z"
        sample_article_4.url = "http://example_url_0.com"
        sample_article_4.index_text = "'v"
        sample_article_4.category = CMR_Index_Categories.extra

        sample_article_5 = Article()
        sample_article_5.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
        sample_article_5.url = "http://example_url_1.com"
        sample_article_5.index_text = "\"ALee Hull, 4th June 2017"
        sample_article_5.category = CMR_Index_Categories.live

        articles = [sample_article_0, sample_article_1,
                    sample_article_2, sample_article_3, 
                    sample_article_4, sample_article_5]

        original_order_articles = list(articles)        

        sort_articles(articles)
        
        expected_order = [4, 3, 2, 0, 5, 1]
        
        for i in range(0,len(articles)):
            this_article = articles[i]
            expected_article = original_order_articles[expected_order[i]]
            self.assertEqual(this_article.title,
                             expected_article.title)
            self.assertEqual(this_article.index_text,
                             expected_article.index_text)
            self.assertEqual(this_article.url,
                             expected_article.url)

if __name__ == '__main__':
    unittest.main()
