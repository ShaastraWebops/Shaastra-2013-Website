from django.conf.urls.defaults import patterns, include, url
from events.views import *

urlpatterns = patterns('',
<<<<<<< HEAD
    url(r'^customtabs/$', CustomTabs()),
    url(r'^questions/$', QuestionsTab()),
    url(r'^mobapp/$', MobAppTab()),
=======
    url(r'^customtabs/', CustomTabs()),
    url(r'^questions/', Questions()),
    url(r'^mobapp/$', MobApp()),
>>>>>>> 766cb1dea1d8405d39835dc9d79366fd7c331e80
    url(r'^tabfile/$', TabFileSubmit()),
    url(r'^$', CoordDashboard()),
    url(r'^questions/add_mcq$', MCQAddEdit(),{'mcq_id':0}),
    url(r'^questions/edit_mcq/(?P<mcq_id>\d)/$', MCQAddEdit()),
)

#these urls will be imported by the root url.
