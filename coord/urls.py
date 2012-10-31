#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from coord.views import *
from submissions.views import *

urlpatterns = patterns(
    '',
    url(r'^submissions/', submissions),
    url(r'^customtabs/', CustomTabs()),
    url(r'^questions/', Questions()),
    url(r'^mobapp/$', MobApp()),
    url(r'^registrations/$', Registrations()),
    url(r'^viewtdpsubmissions/$', ViewTdpSubmissions, name='viewtdpsubmissions'),
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^update/$', AddUpdate),
    url(r'^editupdate/(?P<id>\d+)', EditUpdate),
    url(r'^editevent/(?P<id>\d+)', editevent, name='editevent'),
    url(r'^$', CoordDashboard()),
    )

# these urls will be imported by the root url.
