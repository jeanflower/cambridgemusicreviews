#!/usr/bin/env python3

import unittest

from cmr.cmr_utilities import get_httpresponse


class Test_get_httpresponse(unittest.TestCase):

    def test_get_httpresponse(self):
        print("test_get_httpresponse...")

        url = "http://nosuchpage.html"
        web_page = get_httpresponse(url)

        self.assertEqual(web_page.exists, False);

        url = "http://www.google.co.uk"
        web_page = get_httpresponse(url)

        self.assertEqual(web_page.exists, True);
        self.assertEqual(web_page.soup.title.string, "Google");

if __name__ == '__main__':
    unittest.main()