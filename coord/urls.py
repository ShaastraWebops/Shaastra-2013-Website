from django.conf.urls.defaults import patterns, include, url
from coord.views import *
from submissions.views import *

urlpatterns = patterns('',
    url(r'^submissions/', submissions),
    url(r'^customtabs/', CustomTabs()),
    url(r'^questions/', Questions()),
    url(r'^mobapp/$', MobApp()),
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^update/$', AddUpdate),
    url(r'^editupdate/(?P<id>\d+)', EditUpdate),
    url(r'^$', CoordDashboard()),
)

#these urls will be imported by the root url.
