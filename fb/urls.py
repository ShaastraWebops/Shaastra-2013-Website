#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth import views
from fb.views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                       url(r'^events/(?P<event_name>.+)', events, name='event-list'),                       
                       url(r'^hero/', hero, name='hero'),
                       url(r'^sampark/(?P<place_name>.+)', sampark, name='sampark'),
                       url(r'^$', home, name='home'),
                       )
