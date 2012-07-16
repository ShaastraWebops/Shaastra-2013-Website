from events.models import * 
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
from django.contrib.sites import *
from django.contrib.sitemaps import *
from sitemaps import *

from events.urls import *
from users.urls import *
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

info_dict = {
    'queryset': Event.objects.all(),
    
}


    

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
#Add the name of any url(without captured parameters) in this list for it to appear in the sitemap
sitelist=['home','login','register','register_fb','editprofile','login_fb','authentication_callback','password_change','password_change_done','logout'
,'coorddashboard','tabfile','summary','summarybyevent','summarybyvenue','summarybydate','summarybyeventgenpdf','summarybyvenuegenpdf',
'summarybydategenpdf','corehome','addgroup','addcore','adminhome','all_submissions']


sitemaps= {

#    'event':EventSitemap,
    'pages':SiteSiteMap(sitelist),
    
    'editcoresitemap':EditCoreSiteMap(),
    'editgroupsitemap':EditGroupSiteMap(),
    'editgroupsitemap':Register_ActivateSiteMap(),
    'addsubeventsitemap':AddSubEventSiteMap(),
    'editsubeventsitemap':EditSubEventSiteMap(),
    'deletesubeventsitemap':DeleteSubEventSiteMap(),
    'lockeventsitemap':LockEventSiteMap(),
    'unlockeventsitemap':UnlockEventSiteMap(),
    'event_submissionsitemap':Event_SubmissionSiteMap()

}
urlpatterns += patterns ('',
    #...<snip out other url patterns>...
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$','django.contrib.sitemaps.views.sitemap' , {'sitemaps': sitemaps}),
)


