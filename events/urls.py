#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from events.views import *

urlpatterns = patterns('',
                       url(r'^sponslogo', logo, name='spons-logo'),
                       url(r'^(?P<event_id>\d+)/register/$', register),
                       url(r'^(?P<event_id>\d+)/cancelregistration/$', cancel_registration),
                       #url(r'^(?P<event_name>.+)/tab/(?P<tab_name>.+)', tabs, name='tab-list'),
                       url(r'^(?P<event_name>.+)', events, name='event-list'),
                       url(r'^sampark/', sampark, name='sampark-home'),
                       url(r'^shows/', sampark, name='shows-home'),
                       url(r'^$', home, name='event-home'),
                       )
