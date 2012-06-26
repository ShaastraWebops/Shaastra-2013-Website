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

	# DTV Summary pages - On Screen 
	url(r'^events/DTVSummary/$', dtvSummaryHandler),
	url(r'^events/DTVSummary/ByEvent/$', dtvSummaryByEvent),
	url(r'^events/DTVSummary/ByVenue/$', dtvSummaryByVenue),
	url(r'^events/DTVSummary/ByDate/$', dtvSummaryByDate),

	# DTV Summary pages - PDF Versions
    url(r'^events/DTVSummary/ByEvent/generatePDF/$', dtvSummaryByEvent_PDF),
	url(r'^events/DTVSummary/ByVenue/generatePDF/$', dtvSummaryByVenue_PDF),
	url(r'^events/DTVSummary/ByDate/generatePDF/$', dtvSummaryByDate_PDF),

    # Other urls - add, edit, delete subevents ; lock, unlock events
    url(r'^events/(?P<event>.*)/addSubEvent/$', SubEventAdd()),
    url(r'^events/(?P<event>.*)/(?P<subevent>.*)/editSubEvent/$', SubEventEdit()),
    url(r'^events/(?P<event>.*)/(?P<subevent>.*)/deleteSubEvent/$', SubEventDelete()),
    url(r'^events/(?P<event>.*)/lockEvent/$', LockEvent()),
    url(r'^events/(?P<event>.*)/unlockEvent/$', UnlockEvent()),
)

urlpatterns += DTVFeatureURLs

#these urls will be imported by the root url.
