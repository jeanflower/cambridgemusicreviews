#!/usr/bin/env python3

import unittest

from django.test import TestCase

from indexer.models import CMR_Index_Categories
from cmr_get_articles_from_webpage import get_index_anchors, extend_url_map, get_local_cmr_page

class Test_get_httpresponse(TestCase):

    def test_get_index_anchors(self):

        local_page = get_local_cmr_page()

        html = local_page.html

        #------- GET DATA out of the web page of interest
        soup = local_page.soup

        #Use a sequence of calls to get the anchors out of each div
        articles = get_index_anchors(soup, "cmr-extras", CMR_Index_Categories.extra)
        articles = articles + get_index_anchors(soup, "cmr-singles", CMR_Index_Categories.single_ep)
        articles = articles + get_index_anchors(soup, "cmr-albums", CMR_Index_Categories.album)
        articles = articles + get_index_anchors(soup, "cmr-live", CMR_Index_Categories.live)

        #report back

        self.assertEqual(len(articles), 157)
        for i in range(0, 4):
            self.assertEqual(articles[i].category, CMR_Index_Categories.extra)
        for i in range(4, 25):
            self.assertEqual(articles[i].category, CMR_Index_Categories.single_ep)
        for i in range(25, 63):
            self.assertEqual(articles[i].category, CMR_Index_Categories.album)
        for i in range(63, 157):
            self.assertEqual(articles[i].category, CMR_Index_Categories.live)

        test_url = "https://cambridgemusicreviews.net/2015/12/23/12-highlights-from-2015-a-sampler-of-the-year/"
        test_index_text = "12 Highlights from 2015"

        self.assertEqual(articles[0].title, "")
        self.assertEqual(articles[0].url, test_url)
        self.assertEqual(articles[0].index_text, test_index_text)

        url_map = dict()
        extend_url_map(soup, "cmr-extras", CMR_Index_Categories.extra, url_map)
        extend_url_map(soup, "cmr-singles", CMR_Index_Categories.single_ep, url_map)
        extend_url_map(soup, "cmr-albums", CMR_Index_Categories.album, url_map)
        extend_url_map(soup, "cmr-live", CMR_Index_Categories.live, url_map)
        
        self.assertEqual(url_map[test_url].url, test_url)
        self.assertEqual(url_map[test_url].index_text, test_index_text)

#        print("articles found:")
#        article_number = 0
#        for article in articles:
#            article_number = article_number + 1
#            print("--------- article number "+str(article_number)+" "+article.index_text)
#        #    article.print_article_details()
#        print("done")

        html.close()


if __name__ == '__main__':
    unittest.main()
