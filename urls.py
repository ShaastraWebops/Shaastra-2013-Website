from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import redirect_to
import os


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^', include('forum.urls')),
#    (r'^osqa/', include('forum.urls')),
#    url(r'^m/(?P<skin>\w+)/media/(?P<path>.*)$', 'forum.views.meta.media' , name='osqa_media'),
#    url(r'^%s(?P<path>.*)$' % _('upfiles/'), 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__),'forum', 'upfiles').replace('\\', '/')}, name='uploaded_file',),

#    url(r'^', include ('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

handler404 = 'forum.views.meta.page'
handler500 = 'forum.views.meta.error_handler'