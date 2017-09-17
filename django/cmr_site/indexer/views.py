from django.http import HttpResponse

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
from cmr.cmr_utilities import sort_articles

from indexer.models import Article

def index(request):

    # Create a new database entry
#    a = Article(title = "ABC, Parker’s Piece, Cambridge, 7 July\xa02017",
#                url = "https://cambridgemusicreviews.net/2017/"+\
#                      "07/09/abc-parkers-piece-cambridge-7-july-2017/",
#                index_text = "ABC");
#    a.save()

    articles = get_all_cmr_articles()

    # Popoulate the db with the articles we obtained above
#    print("clear db")
#    Article.objects.all().delete()
#    db_articles = Article.objects.all()
#    print(db_articles)
#    print("populate db")
#    for article in articles:
#        a = Article(title = article.title,
#                    url = article.url,
#                    index_text = article.url,
#                    category = article.category,
#                    index_status = article.index_status);
#        a.save()

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
        sort_articles(articles)
        html = get_index_doc_html(articles)
        return HttpResponse(html)
    else:
        html = get_problem_doc_html(problem_articles)
        return HttpResponse(html)


#def index(request):
#    return HttpResponse("Hello, world. You're at the indexer.")

