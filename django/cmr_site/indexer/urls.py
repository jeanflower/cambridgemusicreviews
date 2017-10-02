from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.cmr_home, name='cmr_home'),
    url(r'^index$', views.index, name='index'),
    url(r'^refresh_from_wp/$', views.refresh_from_wp, name='refresh_from_wp'),
    url(r'^update_from_wp/$', views.update_from_wp, name='update_from_wp'),
    url(r'^get_index_text/(?P<article_id>\d+)$', views.get_index_text, name='get_index_text'),
    url(r'^display_db_index/$', views.display_db_index, name='display_db_index'),
    url(r'^display_db_index_raw/$', views.display_db_index_raw, name='display_db_index_raw'),
    url(r'^display_tagged_db_index/(?P<tag_text>\w+)/(?P<raw_view>\d+)/$', views.display_tagged_db_index, name='display_tagged_db_index'),
    #url(r'^(?P<article_id>[0-9]+)/edit/$', views.edit, name='edit'),
]

