#!/usr/bin/env python3

#import unittest
#
#from cmr_get_articles_from_webpage import get_all_cmr_articles
#
#class Test_get_all_cmr_articles(unittest.TestCase):
#
#    def test_get_all_cmr_articles(self):
#        print("test_get_all_cmr_articles...")
#
#        articles = get_all_cmr_articles()
#
#        self.assertTrue(len(articles) > 100) # currently 145
#
#        titles = set()
#        urls = set()
#        for article in articles:
#
#            # each title has more than 4 characters
#            self.assertTrue(len(article.title) > 4)
#            # each url has more than 15 characters
#            self.assertTrue(len(article.url) > 15)
#
#            titles.add(article.title)
#            urls.add(article.url)
#
#        # each article has unique title and url
#        self.assertEqual(len(articles), len(titles))
#        self.assertEqual(len(articles), len(urls))
#
#if __name__ == '__main__':
#    unittest.main()
