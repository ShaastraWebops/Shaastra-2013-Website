# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from events.views import *

urlpatterns = patterns('',
    url(r'^$', events, name = 'event-list'),
)
