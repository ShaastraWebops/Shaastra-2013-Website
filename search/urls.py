from django.conf.urls.defaults import patterns, include, url
from search.views import searchquery

urlpatterns = patterns(
    '',
    url(r'^(?P<search_term>[^/]+)/$', searchquery),
    )
