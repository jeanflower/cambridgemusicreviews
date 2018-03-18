#!/usr/bin/env python3

import unittest
from django.test import TestCase

from indexer.models import Article, CMR_Index_Categories
from cmr_fill_in_data import fill_in_missing_data

def setup_articles():
        sample_article_0 = Article()
        sample_article_0.title = "ABC, Parker’s Piece, 7 month-year"
        sample_article_0.url = "http://example_url_0.com"

        sample_article_1 = Article()
        sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
        sample_article_1.url = "http://example_url_1.com"
        sample_article_1.index_text = "Lee Hull, 4th Junish 2017"
        sample_article_1.category = CMR_Index_Categories.live

        sample_article_2 = Article()
        sample_article_2.title = "no idea, what this is, 1 month-year"
        sample_article_2.url = "http://example_url_2.com"

        articles = [sample_article_0, sample_article_1, sample_article_2]

        fill_in_missing_data(articles)
        return articles

class Test_fill_in_missing_data(TestCase):

    def test_fill_in_missing_data_01(self):
        articles = setup_articles()

        self.assertEqual(articles[0].title, "ABC, Parker’s Piece, 7 month-year")
        self.assertEqual(articles[0].url, "http://example_url_0.com")
        self.assertEqual(articles[0].index_text, "ABC, 7th month-year")
        self.assertEqual(articles[0].category, CMR_Index_Categories.live)

        self.assertEqual(articles[1].title, "Lee Hull, Corner House, Cambridge, 4 June 2017")
        self.assertEqual(articles[1].url, "http://example_url_1.com")
        self.assertEqual(articles[1].index_text, "Lee Hull, 4th Junish 2017")
        self.assertEqual(articles[1].category, CMR_Index_Categories.live)

        self.assertEqual(articles[2].title, "no idea, what this is, 1 month-year")
        self.assertEqual(articles[2].url, "http://example_url_2.com")
        self.assertEqual(articles[2].index_text, "no idea, what this is, 1 month-year")
        self.assertEqual(articles[2].category, CMR_Index_Categories.extra)

    def test_fill_in_missing_data_02(self):
        gig_dates = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th",
                     "9th", "10th", "11th", "12th", "13th", "14th", "15th",
                     "16th", "17th", "18th", "19th", "20th", "21st", "22nd",
                     "23rd", "24th", "25th", "26th", "27th", "28th", "29th",
                     "30th", "31st"]
        for i in range(1, 32):
            sample_article = Article()
            sample_article.title = "ABC, Parker’s Piece, "+str(i)+" month-year"
            sample_article.url = "http://example_url_0.com"
            articles = [sample_article]

            fill_in_missing_data(articles)

            #print(articles[0].index_text)

            self.assertEqual(articles[0].index_text, \
                             "ABC, "+gig_dates[i-1]+" month-year")


if __name__ == '__main__':
    unittest.main()

