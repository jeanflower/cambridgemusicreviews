#!/usr/bin/env python3

from cmr.cmr_utilities import CMR_Index_Categories

def get_html_link(article):
    html = "<a href=\""
    html = html + article.url
    html = html + "\">"
    html = html + article.index_text
    html = html + "</a><br />\n"
    return html

def get_index_html(articles):
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
    html = html + \
           "</div>\n" +\
           "<!–– stop copying for wordpess here -->\n"
    return html

def save_index_html(articles, filename):
    get_index_html(articles)
    #TODO : save to a file called filename
    html = "<!DOCTYPE html><body>"+get_index_html(articles)+"</body></html>"

    f = open(filename, 'w')
    f.write(html)
    f.close()

