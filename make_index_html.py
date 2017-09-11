from cmr.cmr_utilities import sort_articles

from cmr.cmr_get_articles_from_webpage import get_all_cmr_articles

from cmr.cmr_interactive import fill_in_missing_data_quiet

from cmr.cmr_create_index_html import save_index_html, get_problem_doc_html


articles = get_all_cmr_articles()
problem_articles = []

#for article in articles:
#    article.print_article_details()

if fill_in_missing_data_quiet(articles, problem_articles):

    sort_articles(articles)
    save_index_html(articles, "test.html")

else:

    print("can't identify type(s) for "+get_problem_doc_html(problem_articles))
