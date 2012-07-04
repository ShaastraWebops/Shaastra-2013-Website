# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from admin.views import *

urlpatterns = patterns('',  
    url(r'^$', home, name = 'home'),
)