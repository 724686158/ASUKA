from django.conf.urls import patterns, url
from alchimest import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
)
