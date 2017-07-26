#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def generate_text_for_web_display(request):
    return HttpResponse("Hello World!")

##  Below fails with "No module named 'cmr'"
#
#from cmr.cmr_utilities import sort_articles
#
#from cmr.cmr_get_articles_from_webpage import get_all_cmr_data
#
#from cmr.cmr_interactive import fill_in_missing_data, \
#                                get_missing_index_text_interactive, \
#                                get_missing_category_interactive, \
#                                confirm_is_single_interactive, \
#                                confirm_is_album_interactive, \
#                                confirm_is_live_interactive
#
#from cmr.cmr_create_index_html import get_index_html
#
#def make_index_html():
#    
#    articles = get_all_cmr_data()
#
#    fill_in_missing_data(articles,
#                         get_missing_index_text_interactive,
#                         get_missing_category_interactive,
#                         confirm_is_single_interactive,
#                         confirm_is_album_interactive,
#                         confirm_is_live_interactive)
#    
#    sort_articles(articles)
#
#    return HttpResponse(get_index_html(articles))