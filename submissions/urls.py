from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from submissions.views import *

urlpatterns = patterns('',
    url(r'^$', all_submissions, name = 'sub_home'),
    url(r'^(?P<event_id>\d+)/$', event_submission, name = 'sub_event'),
    url(r'^(?P<eve_id>\d+)/subques/(?P<q_id>\d+)/$', save_edit_subjective, name = 'sub'),
    url(r'^(?P<eve_id>\d+)/mcques/(?P<q_id>\d+)/$', save_edit_mcq, name = 'mcq'),
)
