from indexer.models import Article, CMR_Index_Categories
from cmr_utilities import sort_articles

from cmr_get_articles_from_webpage import get_wp_articles

from cmr_fill_in_data import fill_in_missing_data

from cmr_create_index_html import save_index_html

def example_save_index_html_two_articles():
    
    sample_article_0 = Article()
    sample_article_0.title = "ABC, Parker’s Piece, 7 July 2017"
    sample_article_0.url = "http://example_url_0.com"

    sample_article_1 = Article()
    sample_article_1.title = "Lee Hull, Corner House, Cambridge, 4 June 2017"
    sample_article_1.url = "http://example_url_1.com"
    sample_article_1.index_text = "Lee Hull, 4th June 2017"
    sample_article_1.category = CMR_Index_Categories.live

    articles = [sample_article_0, sample_article_1]

    print("before filling in missing details:")
    for article in articles:
        print("----")
        article.print_article_details()

    fill_in_missing_data(articles)

    save_index_html(articles, "test_output_two_samples.html")

def example_save_index_html():
    articles = get_wp_articles()
    fill_in_missing_data(articles)

    sort_articles(articles)

    save_index_html(articles, "test_output_all_unsorted.html")


if __name__ == '__main__':
    example_save_index_html()