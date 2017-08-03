from django.http import HttpResponse
import sys
sys.path.append('../..')

from importlib import import_module
import_module("cmr.cmr_create_index_html")

from cmr.cmr_get_articles_from_webpage import get_all_cmr_data
from cmr.cmr_interactive import fill_in_missing_data_interactive
from cmr.cmr_create_index_html import get_index_doc_html
from cmr.cmr_utilities import sort_articles

def index(request):
    articles = get_all_cmr_data()
    fill_in_missing_data_interactive(articles)
    sort_articles(articles)
    html = get_index_doc_html(articles)
    return HttpResponse(html)

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

