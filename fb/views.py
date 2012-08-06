#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from events.models import Event, EVENT_CATEGORIES
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from dtvpicker.models import SubEvent
import urllib
import json


@csrf_exempt
def home(request):
    event_set = Event.objects.all()
    for event in event_set:
        if event.fb_event_id and not event.updated:

            # Event needs to be updated

            subevent = SubEvent.objects.filter(event=event)[0]
            event_data = {
                'name': event.title,
                'owner': settings.FACEBOOK_APP_ID,
                'description': event.mobapptab.text,
                'start_time': subevent.start_date_and_time.isoformat(' '
                        ),
                'end_time': subevent.end_date_and_time.isoformat(' '),
                'location': subevent.venue,
                'access_token': '291744470918252|RCjCxoQPQZdXAiWBiURxP81aUm8',
                }
            target = urllib.urlopen('https://graph.facebook.com/'
                                    + event.fb_event_id,
                                    urllib.urlencode(event_data)).read()
        elif not event.fb_event_id:

            # Event needs to be created

            subevent = SubEvent.objects.filter(event=event)[0]
            if subevent:
                event_data = {
                    'name': event.title,
                    'owner': settings.FACEBOOK_APP_ID,
                    'description': event.mobapptab.text,
                    'start_time': subevent.start_date_and_time.isoformat(' '
                            ),
                    'end_time': subevent.end_date_and_time.isoformat(' '
                            ),
                    'location': subevent.venue,
                    'access_token': '291744470918252|RCjCxoQPQZdXAiWBiURxP81aUm8',
                    }
                target = \
                    urllib.urlopen('https://graph.facebook.com/app/events'
                                   ,
                                   urllib.urlencode(event_data)).read()
                response = json.loads(target)
                event.fb_event_id = response['id']
                event.save()
    event_set = []
    for c in EVENT_CATEGORIES:
        event_category_set = Event.objects.filter(category=c[0])
        if event_category_set:
            event_set.append(event_category_set)
    return render_to_response('fb/home.html', locals(),
                              context_instance=RequestContext(request))


@csrf_exempt
def events(request, event_id):
    try:
        temp = (request.META['HTTP_REFERER'])[:23]
        if temp == 'http://www.facebook.com':
            return HttpResponseRedirect(settings.SITE_URL + '#events/'
                    + event_id)
    except:
        pass
    event_set = []
    for c in EVENT_CATEGORIES:
        event_category_set = Event.objects.filter(category=c[0])
        if event_category_set:
            event_set.append(event_category_set)
    event = Event.objects.get(id=event_id)
    event_intro = event.mobapptab.text
    return render_to_response('ajax/fb/events.html', locals(),
                              context_instance=RequestContext(request))
