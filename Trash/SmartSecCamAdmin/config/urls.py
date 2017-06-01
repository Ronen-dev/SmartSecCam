from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wifi/$', views.wifi, name='wifi'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^profiloption/$', views.profiloption, name='profiloption'),
    url(r'^chgmdppost/$', views.chgmdppost, name='chgmdppost'),
]
