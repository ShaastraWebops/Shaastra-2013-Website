from django.conf.urls.defaults import patterns, include, url
from events.views import *

urlpatterns = patterns('',
    url(r'^add/$', EventAdd()),
    url(r'^edit/$', EventEdit()),
    url(r'^dashboard/$', CoordDashboard()),
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^$', all_events),
)

DTVFeatureURLs = patterns('',
	url(r'^events/DTVSummary/$', dtvSummary),
    url(r'^events/DTVSummary/generatePDF/$', dtvSummary_PDF),
    url(r'^events/(?P<event>.*)/addSubEvent/$', SubEventAdd()),
    url(r'^events/(?P<event>.*)/(?P<subevent>.*)/editSubEvent/$', SubEventEdit()),
    url(r'^events/(?P<event>.*)/(?P<subevent>.*)/deleteSubEvent/$', SubEventDelete()),
    url(r'^events/(?P<event>.*)/lockEvent/$', LockEvent()),
    url(r'^events/(?P<event>.*)/unlockEvent/$', UnlockEvent()),
)

urlpatterns += DTVFeatureURLs

#these urls will be imported by the root url.
