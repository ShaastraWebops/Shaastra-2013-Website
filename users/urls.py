# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from users.views import *
import django.contrib.auth.views
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',  
    url(r'^login/$', 'views.method_splitter', {'GET': login_get, 'POST': login_post}),
    url(r'^register/$', 'views.method_splitter', {'GET': register_get, 'POST': register_post}),
    url(r'^register_fb/$', register_post_fb),    
    url(r'^register/activate/(?P<a_key>[\w]+)/?$', 'main_site.users.views.activate'),
    url(r'^editprofile/$', 'views.method_splitter', {'GET': editprofile_get, 'POST': editprofile_post}),
    url(r'^facebook/login/?$', 'users.fb_views.login'),
    url(r'^facebook/authentication_callback/?$', 'users.fb_views.authentication_callback'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^logout/$', 'users.views.logout', name = 'logout'),
    url(r'^$',redirect_to,{'url':'/2013/main/test'}),
#    url(r'^admin/$','users.views.admin', name="super-user"),
)