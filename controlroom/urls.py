#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from controlroom.views import *
import django.contrib.auth.views
from django.views.generic.simple import redirect_to

urlpatterns = patterns(  
    '',
    url(r'^home/$', home),
    url(r'^individual/$', individual),
    url(r'^team/$', team),
    url(r'^bill/(?P<pk>\d+)/(?P<team>\d+)/$', GenerateBill),
    url(r'^addroom/$', AddRoom),
    url(r'^roommap/$', RoomMap),
    url(r'^addmanyrooms/$', AddMultipleRooms),
    url(r'^checkin/(?P<shaastraid>[\w]+)/?$', TeamCheckIn),
    url(r'^details/(?P<id>[\w]+)/?$', RoomDetails),
    url(r'^checkout/$', CheckOut),
    url(r'^register/$', Register),
    url(r'^createteam/$', CreateTeam),
    url(r'^editteam/$', EditTeam),
    url(r'^editprofile/$', EditProfile),
    url(r'^edituserprofile/(?P<shaastraid>[\w]+)/?$', EditUserProfile),
    url(r'^siteregncsv/?$', SiteCSVRegn),
    )
