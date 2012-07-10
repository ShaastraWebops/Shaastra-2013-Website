import datetime
from django.db import models
from django.contrib.sitemaps import *
from django.contrib.auth.models import *
from events.models import *
from django.contrib.sites import *
from datetime import datetime
from django.core.urlresolvers import *
from users.models import *
class EventSitemap(Sitemap):
    changefreq='never'
    priority='0.5'
    def items(self):
        return Event.objects.all()
    def lastmod(self,obj):
        return obj.updated
    def location(self,obj):
        return '/'
class SiteSiteMap(Sitemap):
    def __init__(self,names):
        self.names=names
    def items(self):
        return self.names
    def changefreq(self,obj):
        return 'always'
    def location(self,obj):
        return reverse(obj)
class EditCoreSiteMap(Sitemap):
    changefreq='always'
    prioirity='0.5'
    def items(self):
        allusers=User.objects.all()
        returnset=[]
        for object in allusers:
            if (object.get_profile()).is_core:
                returnset.append(object)
        return returnset
    def location(self,obj):
        return '/editcore/{obj.id}'

