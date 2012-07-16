from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from events.models import *

# Create your views here.

def events(request, event_id=1):
    event = Event.objects.get(id = event_id)
    tab_set = event.tab_set.all()
    return render_to_response('events/events.html',locals(), context_instance= RequestContext(request))

def tabs(request, event_id=1, tab_id=1):
    event = Event.objects.get(id = event_id)
    tab_set = event.tab_set.all()
    tab = tab_set.get(id = tab_id)
    return HttpResponse(tab.text)

