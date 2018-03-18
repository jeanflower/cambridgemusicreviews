#!/usr/bin/env python3

from indexer.models import INDEX_CATEGORY_STRINGS,\
                           CMR_Index_Categories, CMR_Index_Status, html_tags

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
    html = html + "<br>\n"
    return html

def _insert_section(articles, html, highlight_guesses,
                    category):
    class_text = html_tags[category]
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

def _make_index_html(articles, highlight_guesses):
    html = "\n<!–– start copying for wordpress here -->\n"+\
           "<h2>About</h2>\n"+\
           "<p><a href=\"https://cambridgemusicreviews.net/about/\">About this site</a></p>\n"
    
    # This determines the order in which sections appear in html output    
    sections = [CMR_Index_Categories.live, 
                CMR_Index_Categories.album,
                CMR_Index_Categories.single_ep,
                CMR_Index_Categories.extra,
                CMR_Index_Categories.undefined]
    
    for section in sections:
        html = _insert_section(articles, html, highlight_guesses,\
                        section)

    html = html + "<!–– stop copying for wordpress here -->\n"
    return html

def get_index_doc_html(articles):
    index_html_highlighted = _make_index_html(articles, True)
    index_html = _make_index_html(articles, False)
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

