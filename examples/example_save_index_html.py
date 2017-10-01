#from cmr.cmr_get_articles_from_webpage import get_all_cmr_data_quick_test
from cmr.cmr_utilities import CMR_Article, CMR_Index_Categories

from cmr.cmr_get_articles_from_webpage import get_all_cmr_articles

from cmr.cmr_interactive import fill_in_missing_data_interactive

from cmr.cmr_create_index_html import save_index_html

def example_save_index_html():
    sample_article_0 = CMR_Article()
    sample_article_0.title = "ABC, Parker’s Piece, 7 July 2017"
    sample_article_0.url = "http://example_url_0.com"

    sample_article_1 = CMR_Article()
    sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
    sample_article_1.url = "http://example_url_1.com"
    sample_article_1.index_text = "Lee Hull, 4th June 2017"
    sample_article_1.category = CMR_Index_Categories.live

    articles = [sample_article_0, sample_article_1]

    print("before filling in missing details:")
    for article in articles:
        print("----")
        article.print_article_details()

    fill_in_missing_data_interactive(articles)

    save_index_html(articles, "test_output_two_samples.html")


    articles = get_all_cmr_articles()

    fill_in_missing_data_interactive(articles)

    save_index_html(articles, "test_output_all_unsorted.html")
