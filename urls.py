from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('APIs.views',
        
    url(r'^test/$', 'test'),
    url(r'^events/$', 'EventHandler'),
    url(r'^events/(?P<params>.*)/$', 'EventHandler'),
    url(r'^updates/(?P<params>.*)/$', 'UpdateHandler'),
    url(r'^users/(?P<params>.*)/$', 'UserHandler'),
    url(r'^sessions/(?P<params>.*)/$', 'SessionsHandler'),
)
