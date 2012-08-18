#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.auth import views
from fb.views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                        url(r'^events/(?P<event_id>\d+)', events, name='event-list'),
                        url(r'^$', home, name='home'),
                        url(r'^hero/', direct_to_template, {'template': 'fb/hero.html'}, name='hero'),
                        )
