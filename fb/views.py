#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from events.models import Event, EVENT_CATEGORIES,Tag
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from dtvpicker.models import SubEvent
import urllib
import json,cgi
from django.template.defaultfilters import slugify

@csrf_exempt
def home(request):
    '''
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
                    'start_time': subevent.start_date_and_time.isoformat(' '),
                    'end_time': subevent.end_date_and_time.isoformat(' '),
                    'location': subevent.venue,
                    'access_token': '291744470918252|RCjCxoQPQZdXAiWBiURxP81aUm8',
                    }
                target = \
                    urllib.urlopen('https://graph.facebook.com/app/events',
                                   urllib.urlencode(event_data)).read()
                response = json.loads(target)
                event.fb_event_id = response['id']
                event.save()
    '''
    result_list=[]
    for t in Tag.objects.all():
        row=[]
        row.append(str(t.name))
        temp=[]
        for x in t.event_set.all():
            url = slugify(x)
            temp.append([str(x),str(url)])
        row.append(temp)
        result_list.append(row)
    event_set = []
    for c in EVENT_CATEGORIES:
        event_category_set = Event.objects.filter(category=c[0])
        if c[0] == "Sampark":
            pass
        elif event_category_set:
            event_set.append(event_category_set)
    events = Event.objects.all()
    city_set = ['Bengaluru', 'Hyderabad', 'Pune','Coimbatore','Chennai']
    sampark_set=[]
    city_events=[]
    city_events.append('Bengaluru')
    city_events.append(events.filter(title__startswith="B_"))
    sampark_set.append(city_events)
    city_events=[]
    city_events.append('Hyderabad')
    city_events.append(events.filter(title__startswith="H_"))
    sampark_set.append(city_events)
    city_events=[]
    city_events.append('Pune')
    city_events.append(events.filter(title__startswith="P_"))
    sampark_set.append(city_events)
    city_events=[]
    city_events.append('Coimbatore')
    city_events.append(events.filter(title__startswith="C_"))
    sampark_set.append(city_events)
    city_events=[]
    city_events.append('Chennai')
    city_events.append(events.filter(title__startswith="Ch_"))
    sampark_set.append(city_events)
#    assert False
    return render_to_response('fb/home.html', locals(),
                              context_instance=RequestContext(request))

@csrf_exempt
def hero(request):
    target = urllib.urlopen('https://graph.facebook.com/384669854912067/photos').read()
    photos = json.loads(target)["data"]
    srcs=[]
    for photo in photos:
    	srcs.append(photo["images"][0]["source"])
    return render_to_response('fb/hero.html', locals(),
                              context_instance=RequestContext(request))
@csrf_exempt
def events(request, event_name):
    event_name = event_name.replace('-', ' ')
    if event_name=="robo oceana":
    	event_name="robo-oceana"
    elif event_name=="lectures video conferences":
    	event_name="lectures & video conferences"
    event = Event.objects.get(title=event_name)
    try:
        temp = (request.META['HTTP_REFERER'])[:23]
        if temp == 'http://www.facebook.com':
            url=settings.SITE_URL + '#events/' + event.title + '/tab/' + event.tab_set.all()[0].title
            return HttpResponseRedirect(url)
    except:
        pass
#    event_intro = "Desciption comes here!"
    event_intro = event.mobapptab.text
    return render_to_response('ajax/fb/events.html', locals(),
                              context_instance=RequestContext(request))