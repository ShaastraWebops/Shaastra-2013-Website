from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib import *
from django.contrib.auth.models import User
from events.models import *
# Create your views here.

def all_events(request):
    events = Event.objects.all()
    return render_to_response('allevents.html',locals(),context_instance = RequestContext(request))
    
class BaseView(object):
    
    def __call__(self, request, **kwargs):
        method = request.META['REQUEST_METHOD'].upper()
        handler = getattr(self, 'handle_%s' %method, None)
        
        if handler is None:
            methods = []
            for x in dir(self):
                if x.startswith('handle_'):
                    methods.append(x[7:])
            return HttpResponseNotAllowed(methods)
            
        return handler(request, **kwargs)
        
    def get_tabs(self,event):
        try:
            return event.tab_set.all()
        except:
            raise Http404()
        
class EventAdd(BaseView):
    def handle_GET(self, request, **kwargs):
        form = EventAddForm()
        return render_to_response('events/addevent.html', locals(), context_instance = RequestContext(request))
        
    def handle_POST(self, request, **kwargs):
        form = EventAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/events/')
        return render_to_response('events/addevent.html', locals(), context_instance = RequestContext(request))
        
class EventEdit(BaseView):
    def handle_GET(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        form = EventAddForm(instance = event)
        return render_to_response('events/editevent.html', locals(), context_instance = RequestContext(request))
        
    def handle_POST(self, request, **kwargs):
        form = EventAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/events/')
        return render_to_response('events/addevent.html', locals(), context_instance = RequestContext(request))
        
class CoordDashboard(BaseView):
    def handle_GET(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        tabs = self.get_tabs(event)
        return render_to_response('events/dashboard.html', locals(), context_instance = RequestContext(request))
        
    #NO NEED FOR POST SINCE WE ARE USING DAJAX
    def handle_POST(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        tabs = self.get_tabs(event)
        return render_to_response('events/dashboard.html', locals(), context_instance = RequestContext(request))
        
        
        
