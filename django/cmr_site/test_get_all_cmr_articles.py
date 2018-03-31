#!/usr/bin/env python3

import unittest
import requests

from cmr_get_articles_from_webpage import get_wp_articles

class Test_get_wp_articles(unittest.TestCase):

    def test_get_wp_articles(self):
        print("test_get_all_cmr_articles...")

        articles = get_wp_articles()
#        print("got articles...")

        num_articles = len(articles)

        if num_articles == 0:
#            allow for no-connection error
            try:
                ret = requests.get("http://www.googleapis.com/customsearch/v1?parameters")
                returned_code = ret.status_code
                print("returned value is "+str(ret.status_code))

                if returned_code != 200:
                    print("error from REST API request")
                    return

            except requests.exceptions.ConnectionError as err:
                print("no connection for REST API request")
                return

        # print("did we get bcak enough articles?")
        self.assertTrue(num_articles > 100) # currently 145

        titles = set()
        urls = set()
        for article in articles:

            # each title has more than 4 characters
            self.assertTrue(len(article.title) > 4)
            # each url has more than 15 characters
            self.assertTrue(len(article.url) > 15)

            titles.add(article.title)
            urls.add(article.url)

        # each article has unique title and url
        self.assertEqual(num_articles, len(titles))
        self.assertEqual(num_articles, len(urls))

if __name__ == '__main__':
    unittest.main()
