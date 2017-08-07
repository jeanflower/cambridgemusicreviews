from cmr.cmr_utilities import sort_articles

from cmr.cmr_get_articles_from_webpage import get_all_cmr_articles

from cmr.cmr_interactive import fill_in_missing_data_quiet

from cmr.cmr_create_index_html import save_index_html


articles = get_all_cmr_articles()

#for article in articles:
#    article.print_article_details()

fill_in_missing_data_quiet(articles)

sort_articles(articles)

save_index_html(articles, "test.html")

