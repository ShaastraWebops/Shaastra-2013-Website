# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from core.views import *

urlpatterns = patterns('',
    url(r'^addevent/', addevent, name='addevent'),
    url(r'^dashboard/(?P<id>\d+)', eventdashboard, name='event-dashboard'),
    url(r'^editevent/(?P<id>\d+)', editevent, name='editevent'),
    url(r'^dashboard/', include('coord.urls'), name = 'dashboard'),
    url(r'^$', home, name = 'home'),
)
