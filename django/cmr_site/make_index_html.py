from cmr_utilities import sort_articles

from cmr_get_articles_from_webpage import get_wp_articles

from cmr_fill_in_data import fill_in_missing_data

from cmr_create_index_html import save_index_html


articles = get_wp_articles()

#for article in articles:
#    article.print_article_details()

fill_in_missing_data(articles)
sort_articles(articles)
save_index_html(articles, "test_output_all_sorted.html")
