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

urlpatterns = patterns('', 
    url(r'^login/$', 'views.method_splitter', {'GET': login_get, 'POST': login_post},name='login'),
    url(r'^register/$', 'views.method_splitter', {'GET': register_get, 'POST': register_post},name='register'),
    url(r'^register_fb/$', register_post_fb,name='register_fb'),    
    
    url(r'^editprofile/$', 'views.method_splitter', {'GET': editprofile_get, 'POST': editprofile_post},name='editprofile'),
    url(r'^facebook/login/?$', 'users.fb_views.login',name='login_fb'),
    url(r'^facebook/authentication_callback/?$', 'users.fb_views.authentication_callback',name='authentication_callback'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change',name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',name='password_change_done'),
    url(r'^logout/$', 'users.views.logout', name = 'logout'),
    url(r'^$',redirect_to,{'url':'/2013/main/test'}),
#    url(r'^admin/$','users.views.admin', name="super-user"),
)
eventurls=urlpatterns
sitemaps= {

    #'event':EventSitemap,
    #'pages':SiteSiteMap(['logout']),
    
}
urlpatterns += patterns ('',
    #...<snip out other url patterns>...
    (r'^users/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^register/activate/(?P<a_key>[\w]+)/?$', 'users.views.activate',name='register_activate'),
)

