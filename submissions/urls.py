from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from submissions.views import *

urlpatterns = patterns('',
    url(r'^$', all_submissions, name = 'all_submissions'),
    url(r'^(?P<event_id>\d)/$', event_submission, name = 'event_submission'),
)
