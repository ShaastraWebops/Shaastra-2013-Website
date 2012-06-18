from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib import *
from django.contrib.auth.models import User
from events.models import *
from django.conf import settings
import os
# Create your views here.

def all_events(request):
    events = Event.objects.all()
    return render_to_response('allevents.html',locals(),context_instance = RequestContext(request))
    
class BaseView(object):
    # parent class. classes below inherit this
    def __call__(self, request, **kwargs):
        # handles request and dispatches the corresponding handler based on the type of request (GET/POST)
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
        # returns list of all tabs of a particular event
        try:
            return event.tab_set.all()
        except:
            raise Http404()
            
    def get_files(self, tab):
        # returns list of all files of a particular tab
        try:
            return tab.tabfile_set.all()
        except:
            print 'here too'
            raise Http404()
        
    def get_template(self, file_name):
        #this is used to get templates from the path /.../shaastra/events/templates/events/ajax      (*in my case)
        #note - a separate folder for ajax templates.
        #this function opens files (*.html) and returns them as python string.
        filepath = os.path.join(settings.AJAX_TEMPLATE_DIR, file_name)
        f = open(filepath, mode='r')
        return f.read()

        
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
        
class TabFileSubmit(BaseView):
    def handle_POST(self, request, **kwargs):
        from django.conf import settings
        # These were the headers set by the function File() to pass additional data. 
        filename = request.META['HTTP_X_FILE_NAME']
        display_name = request.META['HTTP_X_NAME']
        tab_id = request.META['HTTP_X_TAB_ID']
        
        tab = Tab.objects.get(id = tab_id)
        direc = os.path.join(settings.PROJECT_DIR + settings.MEDIA_URL, 'events', str(tab.event.id), tab._meta.object_name, str(tab.id))
        # note that event and tab IDs and not their titles have been used to create folders so that renaming does not affect the folders
        if not os.path.exists(direc):
            os.makedirs(direc)
        path = os.path.join(direc, filename)
        a = TabFile.objects.get_or_create(tab_file = path)
        # get_or_create returns a tuple whose second element is a boolean which is True if it is creating a new object.
        # the first element is the object that has been created/found.
        if a[1]:
            a[0].url = os.path.join(settings.MEDIA_URL, 'events', str(tab.event.id), tab._meta.object_name, str(tab.id), filename)
            f = open(path, 'w')
            with f as dest:
                req = request
                # Right now the file comes as raw input (in form of binary strings). Unfortunately, this is the only way I know that will make ajax work with file uploads.
                foo = req.read( 1024 )
                while foo:
                    dest.write( foo )
                    foo = req.read( 1024 )
        a[0].title = display_name
        a[0].tab = tab
        a[0].save()
        file_list = self.get_files(tab)

        template = self.get_template('file_list.html')
        t = Template(template).render(RequestContext(request, locals()))
        # the ajax function File() assigns this as the innerHTML of a div after the request has been completed.
        return HttpResponse(t)
        
        
