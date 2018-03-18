from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render

from .forms import EditEntryForm, CATEGORY_CHOICES, \
                   SearchForm, SEARCH_LOCATION_CHOICES

from cmr_get_articles_from_webpage import get_wp_articles
from cmr_fill_in_data import fill_in_missing_data
from cmr_create_index_html import get_index_doc_html
from cmr_utilities import sort_articles

from indexer.models import Article, Tag, categories, html_tags

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
    return result

def _make_articles_from_db():
    db_articles = Article.objects.all()
    articles = []
    for db_article in db_articles:
        articles.append(_make_Article(db_article))
    return articles

def index(request):

    print("in index(request)")
    # Create a new database entry
#    a = Article(title = "ABC, Parker’s Piece, Cambridge, 7 July\xa02017",
#                url = "https://cambridgemusicreviews.net/2017/"+\
#                      "07/09/abc-parkers-piece-cambridge-7-july-2017/",
#                index_text = "ABC");
#    a.save()

    articles = _make_articles_from_db()

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

    fill_in_missing_data(articles)
    return HttpResponse(_make_sorted_html(articles))

def cmr_home(request):

    template = loader.get_template('base.html')
    context = {}
    return HttpResponse(template.render(context, request))

def _save_articles_to_db(articles):
    fill_in_missing_data(articles)
    for article in articles:
        a = Article(title=article.title,#TODO - do we need to copy this?
                    url=article.url,
                    index_text=article.index_text,
                    category=article.category,
                    index_status=article.index_status)
#        print("article id is "+str(a.id)) # has no id yet
        a.save()
#        print("article id after save is "+str(a.id)) # has id now
        for t in article.tags:
            Tag.objects.create(article=a, text=t)
            
def refresh_from_wp(request):
    # Populate the db with the articles we obtained above
    Article.objects.all().delete()
    Tag.objects.all().delete()

    articles = get_wp_articles()
    _save_articles_to_db(articles)

    #db_articles = Article.objects.all()
    #print(db_articles)
    
    html = "<h1>Replaced content after updating from "+\
           "the WordPress site</h1>"+get_index_doc_html(articles)
           
    return render(request, 'indexer/generic.html',
                  {'html_content': html})     

def update_from_wp(request):
    articles = get_wp_articles()

    new_articles = []
    for article in articles:
        db_articles = Article.objects.filter(url=article.url)
        if len(db_articles) == 0:
            new_articles.append(article)
            
    if len(new_articles) == 0:
        template = loader.get_template('indexer/no_new_articles.html')
        context = {}
        return HttpResponse(template.render(context, request))
    
    _save_articles_to_db(articles)

    #db_articles = Article.objects.all()
    #print(db_articles)

    html = "This is a view of new content after updating from "+\
           "the wordpress site<p>"+get_index_doc_html(new_articles)
           
    return render(request, 'indexer/generic.html',
                  {'html_content': html})           
           
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

def display_db_articles( request, db_articles, title, raw_view ):
    articles_by_type = {}
    for category in categories:
        articles_by_type[category] = []
    
    for db_article in db_articles:
        articles_by_type[db_article.category].append(db_article)

#    print(len(articles_extras))
#    print(len(articles_singles))
#    print(len(articles_albums))
#    print(len(articles_live))

    for category in categories:
        sort_articles(articles_by_type[category])

    #show_displayed_html = not raw_view == "1"
    show_raw_html = not raw_view == "0" and not raw_view == 0
    #print("raw_view "+str(raw_view))
    #print("show raw html?"+str(show_raw_html))

    template = loader.get_template('indexer/index.html')
    context = {
        'title'                    : title,
        'show_raw_html'            : show_raw_html}
    
    for category in categories:
        context[html_tags[category]] = articles_by_type[category]
    
    return HttpResponse(template.render(context, request))

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

    return display_db_articles(request, db_articles, "", raw_view)

def get_index_text(request, article_id):
    print("entered get_index_text for id "+article_id)

    db_articles = Article.objects.filter(pk=article_id)
    db_article = db_articles.first()

    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        if form.is_valid():
            db_article.index_text = form.cleaned_data['index_text']
            choice = form.cleaned_data['category_choice']
            #print(choice[0])
            #chosen_category = dict(form.fields['category_choice'].choices)\
            #                      [choice]
            #print(chosen_category)
            db_article.category = int(choice[0])-1
            db_article.save()
            return HttpResponseRedirect('../display_db_index')

    else:

        default_index_text = db_article.index_text
        default_choice = CATEGORY_CHOICES[db_article.category][0]
        #print("default choice = "+str(default_choice))
        form = EditEntryForm(initial={'index_text':default_index_text,
                                      'category_choice':default_choice})

    #print("form is" +str(form))
    return render(request, 'indexer/index_text.html',
                  {'article_id': article_id,
                   'article_title': db_article.title,
                   'article_url' : db_article.url,
                   'article_index_text' : db_article.index_text,
                   'form': form})

def search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            
            search_results = []
            search_locations = form.cleaned_data['location_choice']
            for location in search_locations:
                print(SEARCH_LOCATION_CHOICES[int(location)-1][1])
                if SEARCH_LOCATION_CHOICES[int(location)-1][1] == "Title":
                    search_results = search_results +\
                            list(Article.objects.filter(title__icontains=search_term))
                elif SEARCH_LOCATION_CHOICES[int(location)-1][1] == "Tags":
                    search_results = search_results +\
                            list(Article.objects.filter(tag__text__icontains=search_term))
                elif SEARCH_LOCATION_CHOICES[int(location)-1][1] == "Index text":
                    search_results = search_results +\
                            list(Article.objects.filter(index_text__icontains=search_term))

            return display_db_articles(request, 
                                       set(search_results), 
                                       "Search Results", 
                                       "0")

    else:

        default_search_text = "search_term"
        default_choice = '1'
        form = SearchForm(initial={'':default_search_text,
                                   'location_choice':default_choice})

    #print("form is" +str(form))
    return render(request, 'indexer/search.html',
                  {'form': form})
