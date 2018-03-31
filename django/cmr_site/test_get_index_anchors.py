#!/usr/bin/env python3

import unittest

from django.test import TestCase

from indexer.models import CMR_Index_Categories
from cmr_get_articles_from_webpage import make_url_map_from_local_html_page

class Test_get_httpresponse(TestCase):

    def test_make_url_map(self):

        url_map = make_url_map_from_local_html_page()

        #Use a sequence of calls to get the anchors out of each div
        articles = []
        for article in url_map.values():
            articles.append(article)

        #print(articles[0])

        found_num_extras = 0
        found_num_singles = 0
        found_num_albums = 0
        found_num_live = 0

        for article in articles:
            if article.category == CMR_Index_Categories.extra:
                found_num_extras = found_num_extras + 1
            elif article.category == CMR_Index_Categories.single_ep:
                found_num_singles = found_num_singles + 1
            elif article.category == CMR_Index_Categories.album:
                found_num_albums = found_num_albums + 1
            elif article.category == CMR_Index_Categories.live:
                found_num_live = found_num_live + 1

        #report back

        expected_num_extras = 5
        expected_num_singles = 29
        expected_num_albums = 41
        expected_num_live = 103

        report = ""
        print_report = False;
        if found_num_extras != expected_num_extras:
            print_report = True;
            report += "found_num_extras = "+str(found_num_extras)
        if found_num_singles != expected_num_singles:
            print_report = True;
            report += "found_num_singles = "+str(found_num_singles)
        if found_num_albums != expected_num_albums:
            print_report = True;
            report += "found_num_albums = "+str(found_num_albums)
        if found_num_live != expected_num_live:
            print_report = True;
            report += "found_num_live = "+str(found_num_live)
        if print_report:
            print(report)

        self.assertEqual(found_num_extras, expected_num_extras)
        self.assertEqual(found_num_singles, expected_num_singles)
        self.assertEqual(found_num_albums, expected_num_albums)
        self.assertEqual(found_num_live, expected_num_live)

        type_change_1 = found_num_live + found_num_albums
        type_change_2 = type_change_1 + found_num_singles
        type_change_3 = type_change_2 + found_num_extras

        for i in range(0, found_num_live):
            self.assertEqual(articles[i].category, CMR_Index_Categories.live)
        for i in range(found_num_live, type_change_1):
            self.assertEqual(articles[i].category, CMR_Index_Categories.album)
        for i in range(type_change_1, type_change_2):
            self.assertEqual(articles[i].category, CMR_Index_Categories.single_ep)
        for i in range(type_change_2, type_change_3):
            self.assertEqual(articles[i].category, CMR_Index_Categories.extra)

        # The first article for the first section in
        # indexer.models.categories (currently this is the first "live")
        test_url = "https://cambridgemusicreviews.net/2017/11/07/a-new-routes-special-junction-j3-cambridge-5-november-2017/"
        test_index_text = "‘A New Routes Special’, 5th November 2017"

        self.assertEqual(articles[0].title, "")
        self.assertEqual(articles[0].url, test_url)
        self.assertEqual(articles[0].index_text, test_index_text)

        self.assertEqual(url_map[test_url].url, test_url)
        self.assertEqual(url_map[test_url].index_text, test_index_text)

#        print("articles found:")
#        article_number = 0
#        for article in articles:
#            article_number = article_number + 1
#            print("--------- article number "+str(article_number)+" "+article.index_text)
#        #    article.print_article_details()
#        print("done")

if __name__ == '__main__':
    unittest.main()
