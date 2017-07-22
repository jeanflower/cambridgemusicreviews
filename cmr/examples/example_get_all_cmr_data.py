#!/usr/bin/env python3
from cmr.cmr_get_articles_from_webpage import get_all_cmr_data

articles = get_all_cmr_data()
for article in articles:
    print("---------------")
    article.print_article_details()
    
