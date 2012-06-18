from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from events.urls import urlpatterns as event_urls


urlpatterns = patterns('',
    url(r'^$', 'views.home', name = 'home'),
    url(r'^user/', include('users.urls')),
)

urlpatterns += event_urls

urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)

urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True }),)
