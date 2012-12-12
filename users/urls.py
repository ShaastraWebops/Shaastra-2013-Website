#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
import users
import django.contrib.auth.views
from django.views.generic.simple import redirect_to
from users.views import *
from django.contrib.sites import *
from django.contrib.sitemaps import *
from sitemaps import *
from django.contrib.sites import *

urlpatterns = patterns(  #    url(r'^reset/(?P[0-9A-Za-z]+)-(?P.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    '',
    url(r'^login/$', 'views.method_splitter', {'GET': login_get,
        'POST': login_post}),
    url(r'^register/$', 'views.method_splitter', {'GET': register_get,
        'POST': register_post}),
    url(r'^register_fb/$', register_post_fb),
    url(r'^register/activate/(?P<a_key>[\w]+)/?$',
        'users.views.activate'),
    url(r'^editprofile/$', 'views.method_splitter',
        {'GET': editprofile_get, 'POST': editprofile_post}),
    url(r'^facebook/login/?$', 'users.fb_views.login'),
    url(r'^facebook/authentication_callback/?$',
        'users.fb_views.authentication_callback'),
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change'),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done'),
    url(r'^logout/$', 'users.views.logout', name='logout'),
    url(r'^$', redirect_to, {'url': '/2013/main/test'}),
    url(r'^admin/password_reset/$',
        'django.contrib.auth.views.password_reset',
        name='password_reset'),
    url(r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm'),
    url(r'^reset/done/$',
        'django.contrib.auth.views.password_reset_complete'),
    url(r'^events/$', 'users.views.events'),
    url(r'^ajax_login/$', ajax_login_link),
    )
    
# URLs for teams
urlpatterns += patterns('',
    url(r'^teams/(?P<team_id>\d+)/$', team_home),
    url(r'^teams/create/(?P<event_id>\d+)/$', create_team),
    url(r'^teams/(?P<team_id>\d+)/add_member/$', add_member),
    url(r'^teams/(?P<team_id>\d+)/change_leader/$', change_team_leader),
    url(r'^teams/(?P<team_id>\d+)/drop_out/$', drop_out),
    url(r'^teams/(?P<team_id>\d+)/remove_member/$', remove_member),
    url(r'^teams/(?P<team_id>\d+)/dissolve/$', dissolve_team),
    )

#    url(r'^admin/$','users.views.admin', name="super-user"),
