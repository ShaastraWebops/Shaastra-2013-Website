from django.conf.urls.defaults import patterns, include, url
from events.views import *

urlpatterns = patterns('',
    url(r'^customtabs/', CustomTabs()),
    url(r'^questions/', QuestionsTab()),
    url(r'^mobapp/$', MobAppTab()),
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^$', CoordDashboard()),
)

#these urls will be imported by the root url.
