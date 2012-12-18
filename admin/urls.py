#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from admin.views import *

urlpatterns = patterns(
    '',
    url(r'^addgroup/', addgroup, name='addgroup'),
    url(r'^editgroup/(?P<id>\d+)', editgroup, name='editgroup'),
    url(r'^addcore/', addcore, name='addcore'),
    url(r'^editcore/(?P<id>\d+)', editcore, name='editcore'),
    url(r'^$', home, name='home'),
    )

