from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

# Create your views here.

def events(request, name=""):
    if name :
        event=Event.objects.get(title=name)
        tabs= event.tab_set.all()
        return render_to_response('events/event_detail.html',locals(), context_instance= RequestContext(request))
    else:
        event=Event.objects.all()
        return render_to_response('events/events.html',locals(), context_instance= RequestContext(request))

