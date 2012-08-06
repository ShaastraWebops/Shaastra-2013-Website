#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from dtvpicker.views import dtvSummaryHandler, dtvSummaryByEvent, \
    dtvSummaryByVenue, dtvSummaryByDate, dtvSummaryByEvent_PDF, \
    dtvSummaryByVenue_PDF, dtvSummaryByDate_PDF, SubEventAdd, \
    SubEventEdit, SubEventDelete, LockEvent, UnlockEvent

urlpatterns = patterns(  # DTV Summary pages - On Screen
                         # DTV Summary pages - PDF Versions
                         # Add, edit, delete sub-events
                         # Lock, unlock events
    '',
    url(r'^Summary/$', dtvSummaryHandler),
    url(r'^Summary/ByEvent/$', dtvSummaryByEvent),
    url(r'^Summary/ByVenue/$', dtvSummaryByVenue),
    url(r'^Summary/ByDate/$', dtvSummaryByDate),
    url(r'^Summary/ByEvent/GeneratePDF/$', dtvSummaryByEvent_PDF),
    url(r'^Summary/ByVenue/GeneratePDF/$', dtvSummaryByVenue_PDF),
    url(r'^Summary/ByDate/GeneratePDF/$', dtvSummaryByDate_PDF),
    url(r'^(?P<event>.*)/AddSubEvent/$', SubEventAdd()),
    url(r'^(?P<event>.*)/EditSubEvent/(?P<subevent>.*)/$',
        SubEventEdit()),
    url(r'^(?P<event>.*)/DeleteSubEvent/(?P<subevent>.*)/$',
        SubEventDelete()),
    url(r'^(?P<event>.*)/LockEvent/$', LockEvent()),
    url(r'^(?P<event>.*)/UnlockEvent/$', UnlockEvent()),
    )
