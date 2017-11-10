#!/usr/bin/env python3

from indexer.models import INDEX_CATEGORY_STRINGS,\
                           CMR_Index_Categories, CMR_Index_Status

def _get_html_link(article, highlight_guesses):
    html = ""
    highlighted = False
    if highlight_guesses and article.index_status == CMR_Index_Status.from_code:
        html = html + "<mark>"
        highlighted = True
    html = html + "<a href=\""
    html = html + article.url
    html = html + "\">"
    if article.index_text == "":
        html = html + "no index text"
    else:
        html = html + article.index_text
    html = html + "</a>"
    if highlighted:
        html = html + "</mark>"
    html = html + "<br />\n"
    return html

def _insert_section(articles, html, highlight_guesses,
                    category, class_text):
    section = "<div class=\""+class_text+"\">\n"+\
              "<h2>"+INDEX_CATEGORY_STRINGS[category]+"</h2>\n"+\
              "<p>\n"
    count = 0
    for article in articles:
        if article.category != category:
            continue
        section = section + _get_html_link(article, highlight_guesses)
        count = count + 1
    section = section + "</div>\n"
    if count > 0:
        html += section

    return html

def _get_index_html(articles, highlight_guesses):
    html = "\n<!–– start copying for wordpess here -->\n"+\
           "<h2>About</h2>\n"+\
           "<p><a href=\"https://cambridgemusicreviews.net/about/\">About this site</a></p>\n"

    html = _insert_section(articles, html, highlight_guesses,\
                    CMR_Index_Categories.extra, "cmr-extras")
    html = _insert_section(articles, html, highlight_guesses,\
                    CMR_Index_Categories.single_ep, "cmr-singles")
    html = _insert_section(articles, html, highlight_guesses,\
                    CMR_Index_Categories.album, "cmr-albums")
    html = _insert_section(articles, html, highlight_guesses,\
                    CMR_Index_Categories.live, "cmr-live")
    html = _insert_section(articles, html, highlight_guesses,\
                    CMR_Index_Categories.undefined, "cmr-unclassified")

    html = html + "<!–– stop copying for wordpess here -->\n"
    return html

def get_index_doc_html(articles):
    index_html_highlighted = _get_index_html(articles, True)
    index_html = _get_index_html(articles, False)
    html = "<!DOCTYPE html>"+\
           "<title>Cambridge Music Reviews index</title><body>"+index_html_highlighted+\
           "<p><xmp>"+index_html+"</xmp>"+\
           "</body></html>"
    return html

def save_index_html(articles, filename):
    #TODO : save to a file called filename
    html = get_index_doc_html(articles)
    f = open(filename, 'w')
    f.write(html)
    f.close()


def get_html_problem_link(article):
    html = "<a href=\""
    html = html + article.url
    html = html + "\">"
    html = html + article.title
    html = html + "</a><br />\n"
    return html

def _get_problem_html(articles):
    html = "Problem - not enough information to build index for the "+\
           "following articles:<p>"
    for article in articles:
        html = html + get_html_problem_link(article)
    return html

def get_problem_doc_html(articles):
    html = "<!DOCTYPE html>"+\
           "<title>Cambridge Music Reviews index</title><body>"+\
           _get_problem_html(articles)+"</body></html>"
    return html
