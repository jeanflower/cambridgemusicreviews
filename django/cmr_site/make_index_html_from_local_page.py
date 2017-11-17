from indexer.models import CMR_Index_Categories

from cmr_utilities import get_local_cmr_page, sort_articles

from cmr_get_articles_from_webpage import get_index_anchors

from cmr_fill_in_data import fill_in_missing_data

from cmr_create_index_html import save_index_html

local_page = get_local_cmr_page()

html = local_page.html

#------- GET DATA out of the web page of interest
soup = local_page.soup

#Use a sequence of calls to get the anchors out of each div
articles = get_index_anchors(soup, "cmr-extras", CMR_Index_Categories.extra)
articles = articles + get_index_anchors(soup, "cmr-singles", CMR_Index_Categories.single_ep)
articles = articles + get_index_anchors(soup, "cmr-albums", CMR_Index_Categories.album)
articles = articles + get_index_anchors(soup, "cmr-live", CMR_Index_Categories.live)

html.close()
        
#for article in articles:
#    article.print_article_details()


fill_in_missing_data(articles)
sort_articles(articles)
save_index_html(articles, "test_output_all_sorted.html")
