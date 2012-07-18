from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from fb.views import *

urlpatterns = patterns('',
    url(r'^$', home, name = 'home'),
)
