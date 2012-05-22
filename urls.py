from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
#    url(r'^$', 'shaastra2013.views.home', name='home'),
    url(r'^', include ('Shaastra-2013-Website.users.urls')),
    (r'^accounts/', include('allauth.urls')),
    # url(r'^shaastra2013/', include('shaastra2013.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
