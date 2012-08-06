#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth import views
from fb.views import *

urlpatterns = patterns('', url(r'^events/(?P<event_id>\d+)', events,
                       name='event-list'), url(r'^$', home, name='home'
                       ))
