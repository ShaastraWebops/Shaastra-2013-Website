from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
        
    url(r'^test/$', 'API.APIs.views.test'),
    url(r'^events/$', 'API.APIs.views.EventHandler'),
    url(r'^events/(?P<params>.*)/$', 'API.APIs.views.EventHandler'),
    url(r'^users/(?P<params>.*)/$', 'API.APIs.views.UserHandler'),
    url(r'^sessions/(?P<params>.*)/$', 'API.APIs.views.SessionsHandler'),
)
