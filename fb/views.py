from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from events.models import Event, EVENT_CATEGORIES
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    event_set=[]
    for c in EVENT_CATEGORIES :
        event_category_set = Event.objects.filter(category=c[0])
        if event_category_set :
            event_set.append(event_category_set)
    return render_to_response('fb/home.html',locals(),context_instance = RequestContext(request))

@csrf_exempt
def events(request, event_id):
    event_set=[]
    for c in EVENT_CATEGORIES :
        event_category_set = Event.objects.filter(category=c[0])
        if event_category_set :
            event_set.append(event_category_set)
    event = Event.objects.get(id = event_id)
    event_intro = event.tab_set.all()[0].text
    return render_to_response('ajax/fb/events.html',locals(), context_instance= RequestContext(request))