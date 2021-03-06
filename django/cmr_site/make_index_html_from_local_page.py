from cmr_utilities import sort_articles

from cmr_get_articles_from_webpage import make_url_map_from_local_html_page

from cmr_fill_in_data import fill_in_missing_data

from cmr_create_index_html import save_index_html

# url_map is populated by section in order according to
# categories in models.py
url_map = make_url_map_from_local_html_page()

articles = []
for article in url_map.values():
    articles.append(article)

#for article in articles:
#    article.print_article_details()

fill_in_missing_data(articles)

save_index_html(articles, "test_output_all_unsorted.html")

sort_articles(articles)

save_index_html(articles, "test_output_all_sorted.html")
