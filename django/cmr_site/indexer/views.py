from django.http import HttpResponse
from django.template import loader

#import requests
#def index(request):
#    # see https://developer.wordpress.com/docs/api/1.1/get/sites/%24site/posts/
#    #url = "https://cambridgemusicreviews.net/"
#    url = "https://public-api.wordpress.com/rest/v1.1/sites/cambridgemusicreviews.net/posts"
#    url+= "?number=17"
#    url+= "&context=\"display\""
#    #url+= "&search=\"Dylan\""
#    ret = requests.get(url)
#    returned_code = ret.status_code
#    print("returned value is "+str(ret.status_code))
#    if returned_code == 200:
#        all_posts = ret.json()["posts"]
#        titles = ""
#        for post in all_posts:
#            print(post["title"])
#            titles += "<p>"+post["title"]+"\n"
#        return HttpResponse(titles)
#    else:
#        print("not a 200 response")

import sys
sys.path.append('../..')

from importlib import import_module
import_module("cmr.cmr_create_index_html")

from cmr.cmr_get_articles_from_webpage import get_all_cmr_articles
from cmr.cmr_interactive import fill_in_missing_data_quiet
from cmr.cmr_create_index_html import get_index_doc_html, get_problem_doc_html
from cmr.cmr_utilities import sort_articles, CMR_Index_Categories

from indexer.models import Article, Tag

def _make_sorted_html(articles):
    sort_articles(articles)
    return get_index_doc_html(articles)

def _make_Article(db_article):
    result = Article()
    result.title = db_article.title
    result.url = db_article.url
    result.index_text = db_article.index_text
    result.category = db_article.category
    result.index_status = db_article.index_status
    result.tags=[]
    return result

def _make_articles_from_db():
    db_articles = Article.objects.all()
    articles=[]
    for db_article in db_articles:
        articles.append(_make_Article(db_article))
    return articles

def index(request):

    # Create a new database entry
#    a = Article(title = "ABC, Parker’s Piece, Cambridge, 7 July\xa02017",
#                url = "https://cambridgemusicreviews.net/2017/"+\
#                      "07/09/abc-parkers-piece-cambridge-7-july-2017/",
#                index_text = "ABC");
#    a.save()

    articles = get_all_cmr_articles()

    #db_articles = Article.objects.all()
    #print(db_articles)

    # Search the DB
#    result = Article.objects.filter(title__contains="ABC") # succeeds
#    if len(result) == 0:
#        print("no entry like this")
#    else:
#        print(result)
#    result = Article.objects.filter(title__contains="ABCZ") # fails
#    if len(result) == 0:
#        print("no entry like this")
#    else:
#        print(result)

    problem_articles = []
    if fill_in_missing_data_quiet(articles, problem_articles):
        return HttpResponse(_make_sorted_html(articles))
    else:
        html = get_problem_doc_html(problem_articles)
        return HttpResponse(html)


#def index(request):
#    return HttpResponse("Hello, world. You're at the indexer.")

def refresh_from_wp(request):
    articles = get_all_cmr_articles()

    # Populate the db with the articles we obtained above
    Article.objects.all().delete()
    Tag.objects.all().delete()
    for article in articles:
        a = Article(title = article.title,
                    url = article.url,
                    index_text = article.index_text,
                    category = article.category,
                    index_status = article.index_status);
        a.save()
        for t in article.tags:
            Tag.objects.create(article = a, text = t)

    #db_articles = Article.objects.all()
    #print(db_articles)
    
    html = "This is an unsorted view of content as refreshed from "+\
           "the wordpress site<p>"+get_index_doc_html(articles)
    return HttpResponse(html)

def display_db_index(request):
    articles = _make_articles_from_db()
    return HttpResponse("Current db content : "+_make_sorted_html(articles))

white_list_of_tag_text_values = ["live", "album", "single", "EP"]

def display_tagged_db_index(request, tag_text):
    # Only pass whitelisted tag_text values into DB
    # While any tags are possible on WordPress, we protect our DB
    if not tag_text in white_list_of_tag_text_values:
        return HttpResponse("not-approved tag text value "+\
                            "(only "+str(white_list_of_tag_text_values)+" allowed)")
    
    db_articles = Article.objects.filter(tag__text__contains = tag_text)

    articles_extras=[]
    articles_singles=[]
    articles_albums=[]
    articles_live=[]
    articles_unclassified=[]
    for db_article in db_articles:
        if db_article.category == CMR_Index_Categories.extra:
            articles_extras.append(_make_Article(db_article))
        elif db_article.category == CMR_Index_Categories.single_ep:
            articles_singles.append(_make_Article(db_article))
        elif db_article.category == CMR_Index_Categories.album:
            articles_albums.append(_make_Article(db_article))
        elif db_article.category == CMR_Index_Categories.live:
            articles_live.append(_make_Article(db_article))
        else:
            articles_unclassified.append(_make_Article(db_article))
    
    print(len(articles_extras))
    print(len(articles_singles))
    print(len(articles_albums))
    print(len(articles_live))
    
    template = loader.get_template('indexer/index.html')
    context = {
        'article_list_extras'      : articles_extras,
        'article_list_singles'     : articles_singles,
        'article_list_albums'      : articles_albums,
        'article_list_live'        : articles_live,
        'article_list_unclassified': articles_unclassified,
    }
    return HttpResponse("Current db content : "+template.render(context, request))
