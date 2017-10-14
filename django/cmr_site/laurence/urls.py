from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^message$', views.message, name='message'),    
    url(r'^messages$', views.messages, name='messages'),    
    url(r'^codes/(?P<message>\w+)/(?P<shift>\d+)$', views.codes, name = 'codes'),
]

