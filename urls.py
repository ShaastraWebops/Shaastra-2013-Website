from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home', name = 'home'),
    url(r'^user/', include('users.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^coord/', include('events.urls')),
    url(r'^submission/', include('submissions.urls')),
    url(r'^DTVPicker/', include('dtvpicker.urls')),
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

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
