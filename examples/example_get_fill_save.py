#!/usr/bin/env python3

from cmr.cmr_utilities import sort_articles

from cmr.cmr_get_articles_from_webpage import get_all_cmr_data

from cmr.cmr_interactive import fill_in_missing_data, \
             get_missing_index_text_interactive, \
             get_missing_category_interactive, \
             confirm_is_single_interactive, \
             confirm_is_album_interactive, \
             confirm_is_live_interactive

from cmr.cmr_create_index_html import save_index_html

def example_get_fill_save():

    articles = get_all_cmr_data()

    fill_in_missing_data(articles,
                         get_missing_index_text_interactive,
                         get_missing_category_interactive,
                         confirm_is_single_interactive,
                         confirm_is_album_interactive,
                         confirm_is_live_interactive)

    sort_articles(articles)

    save_index_html(articles, "test.html")


