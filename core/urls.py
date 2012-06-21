# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from shaastra.core.views import *

urlpatterns = patterns('',  
    url(r'^$', home, name = 'home'),
)
