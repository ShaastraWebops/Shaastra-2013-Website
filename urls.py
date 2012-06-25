from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from events.urls import urlpatterns as event_urls

import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'Shaastra-2013-Website.views.home', name = 'home'),
    url(r'^login/$', 'views.method_splitter', {'GET': views.login_get, 'POST': views.login_post}),
    url(r'^register/$', 'views.method_splitter', {'GET': views.register_get, 'POST': views.register_post}),
    url(r'^logout/$', 'views.log_out', name = 'logout'),
    # Examples:
    # url(r'^$', 'shaastra2013.views.home', name='home'),
    # url(r'^shaastra2013/', include('shaastra2013.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
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
