from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to
import os


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^', include('forum.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

handler404 = 'forum.views.meta.page'
handler500 = 'forum.views.meta.error_handler'