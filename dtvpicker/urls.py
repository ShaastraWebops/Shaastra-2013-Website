from django.conf.urls.defaults import patterns, url

from dtvpicker.views import dtvSummaryHandler, dtvSummaryByEvent, dtvSummaryByVenue, dtvSummaryByDate, \
                            dtvSummaryByEvent_PDF, dtvSummaryByVenue_PDF, dtvSummaryByDate_PDF, \
                            SubEventAdd, SubEventEdit, SubEventDelete, \
                            LockEvent, UnlockEvent

urlpatterns = patterns('',

	# DTV Summary pages - On Screen
	url(r'^Summary/$', dtvSummaryHandler,name='summary'),
	url(r'^Summary/ByEvent/$', dtvSummaryByEvent,name='summarybyevent'),
	url(r'^Summary/ByVenue/$', dtvSummaryByVenue,name='summarybyvenue'),
	url(r'^Summary/ByDate/$', dtvSummaryByDate,name='summarybydate'),

	# DTV Summary pages - PDF Versions
    url(r'^Summary/ByEvent/GeneratePDF/$', dtvSummaryByEvent_PDF,name='summarybyeventgenpdf'),
	url(r'^Summary/ByVenue/GeneratePDF/$', dtvSummaryByVenue_PDF,name='summarybyvenuegenpdf'),
	url(r'^Summary/ByDate/GeneratePDF/$', dtvSummaryByDate_PDF,name='summarybydategenpdf'),

    # Add, edit, delete sub-events
    url(r'^(?P<event>.*)/AddSubEvent/$', SubEventAdd()),
    url(r'^(?P<event>.*)/EditSubEvent/(?P<subevent>.*)/$', SubEventEdit()),
    url(r'^(?P<event>.*)/DeleteSubEvent/(?P<subevent>.*)/$', SubEventDelete()),
    
    # Lock, unlock events
    url(r'^(?P<event>.*)/LockEvent/$', LockEvent()),
    url(r'^(?P<event>.*)/UnlockEvent/$', UnlockEvent()),
)
