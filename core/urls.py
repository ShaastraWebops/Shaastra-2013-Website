# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from core.views import *

urlpatterns = patterns('',  
    url(r'^$', home, name = 'home'),
)