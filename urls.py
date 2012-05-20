from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Shaastra-2013-Website.portal.views.home', name='home'),
    url(r'^category/$', 'Shaastra-2013-Website.portal.views.category', name='category'),
    url(r'^category/(?P<category>\w+)/$', 'Shaastra-2013-Website.portal.views.events', name='events'),
	url(r'^topic/(?P<topic_url_name>\w+)/$','Shaastra-2013-Website.portal.views.topic_details',name='topic_details'),
    # url(r'^spons_portal/', include('spons_portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
)
