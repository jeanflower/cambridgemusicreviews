#!/usr/bin/env python3

from cmr.cmr_utilities import CMR_Index_Categories

def get_html_link(article):
    html = "<a href=\""
    html = html + article.url
    html = html + "\">"
    if article.index_text=="":
        html = html + "no index text"
    else:
        html = html + article.index_text
    html = html + "</a><br />\n"
    return html

def _get_index_html(articles):
    html = "\n<!–– start copying for wordpess here -->\n"+\
           "<h2>About</h2>\n"+\
           "<p><a href=\"https://cambridgemusicreviews.net/about/\">About this site</a></p>\n"+\
           "<div class=\"cmr-extras\">\n"+\
           "<h2>Extras</h2>\n"+\
           "<p>\n"
    for article in articles:
        if article.category != CMR_Index_Categories.extra :
            continue
        html = html + get_html_link(article);
    html = html + "</div>\n"+\
           "<div class=\"cmr-singles\">\n"+\
           "<h2>Singles and EPs</h2>\n"+\
           "<p>\n"
    for article in articles:
        if article.category != CMR_Index_Categories.single_ep :
            continue
        html = html + get_html_link(article);
    html = html + "</div>\n"+\
           "<div class=\"cmr-albums\">\n"+\
           "<h2>Album reviews</h2>\n"+\
           "<p>\n"
    for article in articles:
        if article.category != CMR_Index_Categories.album :
            continue
        html = html + get_html_link(article);
    html = html + "</div>\n"+\
           "<div class=\"cmr-live\">\n"+\
           "<h2>Live reviews</h2>\n"+\
           "<p>\n"
    for article in articles:
        if article.category != CMR_Index_Categories.live :
            continue
        html = html + get_html_link(article);
    html = html + "</div>\n"+\
           "<div class=\"cmr-unclassified\">\n"+\
           "<h2>No Category</h2>\n"+\
           "<p>\n"
    for article in articles:
        if article.category != CMR_Index_Categories.undefined :
            continue
        html = html + get_html_link(article);
    html = html + \
           "</div>\n" +\
           "<!–– stop copying for wordpess here -->\n"
    return html

def get_index_doc_html(articles):
    index_html = _get_index_html(articles)
    html = "<!DOCTYPE html><body>"+index_html+\
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
    html = "Problem - not enough information to build index for the following articles:<p>"
    for article in articles:
        html = html + get_html_problem_link(article);
    return html

def get_problem_doc_html(articles):
    html = "<!DOCTYPE html><body>"+_get_problem_html(articles)+"</body></html>"
    return html

