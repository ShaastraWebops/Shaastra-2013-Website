from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'search.views.home', name='home'),
    url(r'^addevent/$','search.views.addevent',name='addevent'),
    url(r'^eventdetails/(\d+)/$','search.views.eventdetails',name='eventdetails'),
    url(r'^event/(\d+)/$','search.views.event',name='event'),
    url(r'^event/(\d+)/(\d+)/$','search.views.edittag',name='edittag'),
    url(r'^main/$','search.views.main',name='mainpage'),
    url(r'^main/search/$','search.views.search',name='search'), #used to get results of search bar
    
    # Examples:
    # url(r'^$', 'shaastra2013.views.home', name='home'),
    # url(r'^shaastra2013/', include('shaastra2013.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
