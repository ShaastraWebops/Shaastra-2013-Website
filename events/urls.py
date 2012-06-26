from django.conf.urls.defaults import patterns, include, url
from events.views import *

urlpatterns = patterns('',
    url(r'^add/$', EventAdd()),
    url(r'^edit/$', EventEdit()),
    url(r'^dashboard/$', CoordDashboard()),
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^$', all_events),
)

#these urls will be imported by the root url.
