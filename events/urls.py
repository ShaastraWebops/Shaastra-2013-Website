from django.conf.urls.defaults import patterns, include, url
from events.views import *

urlpatterns = patterns('',
    url(r'^$', CoordDashboard(),name='coorddashboard'),
    url(r'^tabfile/$', TabFileSubmit(),name='tabfile'),
)

#these urls will be imported by the root url.
