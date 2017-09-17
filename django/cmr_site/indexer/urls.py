from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^refresh_from_wp/$', views.refresh_from_wp, name='refresh_from_wp'),
    url(r'^display_db_index/$', views.display_db_index, name='display_db_index'),
    url(r'^display_tagged_db_index/(?P<tag_text>\w+)/(?P<raw_view>\d+)/$', views.display_tagged_db_index, name='display_tagged_db_index'),
]

