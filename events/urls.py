from django.conf.urls.defaults import patterns, include, url
from events.views import *

urlpatterns = patterns('',
    url(r'^$', CoordDashboard()),
    url(r'^tabfile/$', TabFileSubmit()),
)

#these urls will be imported by the root url.
