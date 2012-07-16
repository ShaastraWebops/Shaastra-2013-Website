# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from events.views import *

urlpatterns = patterns('',
    url(r'^(?P<event_id>\d+)/tab/(?P<tab_id>\d+)', tabs, name = 'tab-list'),
    url(r'^(?P<event_id>\d+)', events, name = 'event-list'),
)
