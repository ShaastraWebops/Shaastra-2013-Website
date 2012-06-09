from django.conf.urls.defaults import patterns, include, url
from events.views import *

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
from django.conf import settings
urlpatterns = patterns('',
    url(r'^events/$', all_events),
    url(r'^events/add/$', EventAdd()),
    url(r'^events/edit/$', EventEdit()),
    url(r'^dashboard/$', CoordDashboard()),
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

#these urls will be imported by the root url.
