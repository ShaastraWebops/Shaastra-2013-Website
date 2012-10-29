#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.sitemaps import *
from django.contrib.auth.models import *
from events.models import *
from django.contrib.sites import *
from django.core.urlresolvers import *
from users.models import *
from django.core.urlresolvers import reverse
from settings import SITE_URL
from admin.urls import *
from users.urls import *
from dtvpicker.models import *
from dtvpicker.urls import *
from submissions.urls import *
from django.template.defaultfilters import slugify


# For simple urls

class EventSitemap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):

       # return '/#events/' + slugify(obj.title)
        try :
            tab_name=Tab.objects.filter(event=obj).order_by('pref')[0].title
	except:
	    tab_name=""
	if obj.title.split('_')[0].__len__() ==1 :
	    return '/2013/main/events/sampark/#!events/' + slugify(obj.title)
        return '/2013/main/#!events/' + slugify(obj.title)


class SiteSiteMap(Sitemap):

    def __init__(self, names):
        self.names = names

    def items(self):
        return self.names

    def changefreq(self, obj):
        return 'always'

    def location(self, obj):
        try:
            if obj != None:
                return reverse(obj, args=[obj.pk])
            else:
                return reverse(obj)
        except:
            return str(obj)


# admin captured parameter urls start

class EditCoreSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allusers = UserProfile.objects.all()
        returnset = []
        for object in allusers:

            # profile=UserProfile.objects.filter(id=object.id)

            if object:
                if object.is_core:
                    returnset.append(object)
        return returnset

    def location(self, obj):
        return '/editcore/' + str(obj.id)


class EditGroupSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allgroups = Group.objects.all()
        returnset = []
        for object in allgroups:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/editgroup/' + str(obj.id)


# admin captured parameter urls end
# users captured parameter urls start
# users captured parameter urls end
# dtvpicker captured parameter urls start

class AddSubEventSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allevents = Event.objects.all()
        returnset = []
        for object in allevents:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/' + str(obj.title) + '/AddSubEvent/'


class EditSubEventSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allsubevents = SubEvent.objects.all()
        returnset = []
        for object in allsubevents:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/' + str(obj.event.title) + '/EditSubEvent/' \
            + str(obj.title)


class DeleteSubEventSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allsubevents = SubEvent.objects.all()
        returnset = []
        for object in allsubevents:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/' + str(obj.event.title) + '/DeleteSubEvent/' \
            + str(obj.title)


class LockEventSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allevents = Event.objects.all()
        returnset = []
        for object in allevents:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/' + str(obj.title) + '/LockEvent/'


class UnlockEventSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allevents = Event.objects.all()
        returnset = []
        for object in allevents:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/' + str(obj.title) + '/UnlockEvent/'


# dtvpicker captured parameter urls end here
# submissions captured parameter urls start here

class Event_SubmissionSiteMap(Sitemap):

    changefreq = 'always'
    priority = '0.5'

    def items(self):
        allevents = Event.objects.all()
        returnset = []
        for object in allevents:
            returnset.append(object)
        return returnset

    def location(self, obj):
        return '/' + str(obj.id) + '/'


# submissions captured parameter urls end here