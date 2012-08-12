#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from settings import SITE_URL
from django.contrib.auth import views
from django.contrib.sites import *
from django.contrib.sitemaps import *
from sitemaps import *
from users.urls import *
from events.urls import *
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
from django.contrib import admin as superuser
superuser.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'views.home', name='home'),
    url(r'^user/', include('users.urls')),
    (r'^search/', include('search.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^coord/', include('coord.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^fb/', include('fb.urls')),
    url(r'^submission/', include('submissions.urls')),
    url(r'^DTVPicker/', include('dtvpicker.urls')),
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX,
        include('dajaxice.urls')),
    url(r'^superuser/', include(superuser.site.urls)),
    )

urlpatterns += patterns('', url(r'^media/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns('django.views.static', (r'^static/(?P<path>.*)$'
                        , 'serve',
                        {'document_root': settings.STATIC_ROOT,
                        'show_indexes': True}))

base_url_name = '/2013/main/test/'
sitelist = [base_url_name, base_url_name + '#events/', base_url_name
            + 'user/login/']

sitemaps = {'event': EventSitemap, 'sites': Sitemap,
            'pages': SiteSiteMap(sitelist)}

#    'flatpages':FlatPageSitemap,
#    'editcoresitemap':EditCoreSiteMap(),
#    'editgroupsitemap':EditGroupSiteMap(),
#    'editgroupsitemap':Register_ActivateSiteMap(),
#    'addsubeventsitemap':AddSubEventSiteMap(),
#    'editsubeventsitemap':EditSubEventSiteMap(),
#    'deletesubeventsitemap':DeleteSubEventSiteMap(),
#    'lockeventsitemap':LockEventSiteMap(),
#    'unlockeventsitemap':UnlockEventSiteMap(),
#    'event_submissionsitemap':Event_SubmissionSiteMap()

urlpatterns += patterns('', (r'^sitemap\.xml$',
                        'django.contrib.sitemaps.views.sitemap',
                        {'sitemaps': sitemaps}),
                        (r'^sitemap-(?P<section>.+)\.xml$',
                        'django.contrib.sitemaps.views.sitemap',
                        {'sitemaps': sitemaps}))  # ...<snip out other url patterns>...
