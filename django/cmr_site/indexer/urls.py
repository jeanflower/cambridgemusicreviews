from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^refresh_from_wp/$', views.refresh_from_wp, name='refresh_from_wp'),
    url(r'^display_db_index/$', views.display_db_index, name='display_db_index'),
]

