import sys
sys.path.append('../..')
#sys.path.append("/home/jeanflower/cambridgemusicreviews/cambridgemusicreviews")

from importlib import import_module

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render

from .forms import IndexTextForm, CHOICES

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
    result.tags = []
    return result

def _make_articles_from_db():
    db_articles = Article.objects.all()
    articles = []
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

def cmr_home(request):

    html = "<a href = \"index\">index</a>"+\
    " is a non-persistent way of generating index, guessing categories,"+\
    " highlighting 'new' items (contact admin to update what constitutes \"new\")<p>"+\
    "<a href = \"refresh_from_wp\">refresh_from_wp</a>"+\
    " (SLOW!) clears DB, visits wp, populates DB, presents view of data<p>"+\
    "<a href = \"display_db_index\">display_db_index</a>"+\
    " displays current db content, allows edit of entries<p>"+\
    "<a href = \"display_db_index_raw\">display_db_index_raw</a>"+\
    " displays current db content, raw html<p>"+\
    ""
    return HttpResponse(html)


def _db_sort_key(article):
    result = ""
    if article.index_text[:3] == "The":
        result += article.index_text[4:].strip()
    else:
        result += article.index_text.strip()
    #print(result)
    return result

def _sort_db_articles(articles):
    articles.sort(key=_db_sort_key)


#def index(request):
#    return HttpResponse("Hello, world. You're at the indexer.")

def refresh_from_wp(request):
    articles = get_all_cmr_articles()

    # Populate the db with the articles we obtained above
    Article.objects.all().delete()
    Tag.objects.all().delete()
    for article in articles:
        a = Article(title=article.title,
                    url=article.url,
                    index_text=article.index_text,
                    category=article.category,
                    index_status=article.index_status)
#        print("article id is "+str(a.id)) # has no id yet
        a.save()
#        print("article id after save is "+str(a.id)) # has id now
        for t in article.tags:
            Tag.objects.create(article=a, text=t)

    #db_articles = Article.objects.all()
    #print(db_articles)

    html = "This is a view of content as refreshed from "+\
           "the wordpress site<p>"+get_index_doc_html(articles)
    return HttpResponse(html)

def display_db_index(request):
    raw_view = "0"
    return display_tagged_db_index(request, "all", raw_view)

def display_db_index_raw(request):
    raw_view = "1"
    return display_tagged_db_index(request, "all", raw_view)

white_list_of_tag_text_values = ["live", "album", "single", "EP", "all"]

# raw_view = 0 : show formatted html
# raw_view = 1 : show raw html
# raw_view = 2 : show formatted html then raw HTML


def display_tagged_db_index(request, tag_text, raw_view):

    # Only pass whitelisted tag_text values into DB
    # While any tags are possible on WordPress, we protect our DB
    if not tag_text in white_list_of_tag_text_values:
        return HttpResponse("not-approved tag text value "+\
                            "(only "+str(white_list_of_tag_text_values)+" allowed)")
    if tag_text == "all":
        db_articles = Article.objects.all()
    else:
        db_articles = Article.objects.filter(tag__text__contains=tag_text)

    articles_extras = []
    articles_singles = []
    articles_albums = []
    articles_live = []
    articles_unclassified = []
    for db_article in db_articles:
        if db_article.category == CMR_Index_Categories.extra:
            articles_extras.append(db_article)
        elif db_article.category == CMR_Index_Categories.single_ep:
            articles_singles.append(db_article)
        elif db_article.category == CMR_Index_Categories.album:
            articles_albums.append(db_article)
        elif db_article.category == CMR_Index_Categories.live:
            articles_live.append(db_article)
        else:
            articles_unclassified.append(db_article)


#    print(len(articles_extras))
#    print(len(articles_singles))
#    print(len(articles_albums))
#    print(len(articles_live))

    _sort_db_articles(articles_extras)
    _sort_db_articles(articles_singles)
    _sort_db_articles(articles_albums)
    _sort_db_articles(articles_live)
    _sort_db_articles(articles_unclassified)

    #show_displayed_html = not raw_view == "1"
    show_raw_html = not raw_view == "0"
    print("raw_view "+str(raw_view))
    print("show raw html?"+str(show_raw_html))

    template = loader.get_template('indexer/index.html')
    context = {
        'show_raw_html'            : show_raw_html,
        'article_list_extras'      : articles_extras,
        'article_list_singles'     : articles_singles,
        'article_list_albums'      : articles_albums,
        'article_list_live'        : articles_live,
        'article_list_unclassified': articles_unclassified,
    }
    return HttpResponse(template.render(context, request))

def get_index_text(request, article_id):
    print("entered get_index_text for id "+article_id)

    db_articles = Article.objects.filter(pk=article_id)
    db_article = db_articles.first()

    if request.method == 'POST':
        form = IndexTextForm(request.POST)
        if form.is_valid():
            db_article.index_text = form.cleaned_data['index_text']
            choice = form.cleaned_data['category_choice']
            print(choice[0])
            #chosen_category = dict(form.fields['category_choice'].choices)\
            #                      [choice]
            #print(chosen_category)
            db_article.category = int(choice[0])-1
            db_article.save()
            return HttpResponseRedirect(article_id)

    else:

        default_index_text = db_article.index_text
        default_choice = CHOICES[db_article.category][0]
        print("default choice = "+str(default_choice))
        form = IndexTextForm(initial={'index_text':default_index_text,
                                      'category_choice':default_choice})

    #print("form is" +str(form))
    return render(request, 'indexer/index_text.html',
                  {'article_id': article_id,
                   'article_title': db_article.title,
                   'article_url' : db_article.url,
                   'article_index_text' : db_article.index_text,
                   'form': form})
