from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from events.models import *
from events.forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django import forms

import os
import datetime
from datetime import date

# Create your views here.

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
        

class ProtectedView(BaseView):
    """
    ProtectedView requires users to authenticate themselves before proceeding to the computation logic.
    """

    @method_decorator(login_required)
    def userAuthentication(self, request, **kwargs):
        return True
    
    def __call__(self, request, **kwargs):
        """
        * Checks authentication
        * Handles request
        * Dispatches the corresponding handler based on the type of request (GET/POST)
        """
        # TODO(Anant, anant.girdhar@gmail.com): Instead of copying the code, it would be better if we override BaseView.__call__
        #                                       and add the necessary lines for authentication.
        
        # Copied code from BaseView.__call__
        # Overriding BaseView.__call__ to check authentication.

        if self.userAuthentication(request, **kwargs) == False:
            return HttpResponseForbidden()
        method = request.META['REQUEST_METHOD'].upper()
        handler = getattr(self, 'handle_%s' %method, None)
        
        if handler is None:
            methods = []
            for x in dir(self):
                if x.startswith('handle_'):
                    methods.append(x[7:])
            return HttpResponseNotAllowed(methods)    
        return handler(request, **kwargs)
        
class CoordProtectedView(ProtectedView):
    """
    CoordProtectedView requires the user to be authenticated and to be a coord before proceeding to the computation logic.
    """
    @method_decorator(login_required)
    def userAuthentication(self, request, **kwargs):
        if request.user.get_profile().is_coord_of is not None:
            return True
        return False

    def permissionsGranted(self, request, **kwargs):
        """
        Checks if the coord has permissions to access the requested event.
        """
        try:
            if request.user.get_profile().is_coord_of != Event.objects.get(title = kwargs['event']):
                return False  # If the coord is not coord of the requested event
            return True
        except:
            raise Http404('You do not have permissions to view this page')
        
class CoreProtectedView(ProtectedView):
    """
    CoreProtectedView requires the user to be authenticated and to be a core before proceeding to the computation logic.
    """
    @method_decorator(login_required)
    def userAuthentication(self, request, **kwargs):
        if request.user.get_profile().is_core:
            return True
        return False
    
class CoordDashboard(CoordProtectedView):
    """
    displays the coord dashboard depending on the logged in coords event
    """
    def handle_GET(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        tabs = self.get_tabs(event)
        return render_to_response('events/dashboard.html', locals(), context_instance = RequestContext(request))
        
class TabFileSubmit(CoordProtectedView):
    """
    ajax file uploads are directed to this view
    """
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

        template = loader.get_template('ajax/events/file_list.html')
        t = template.render(RequestContext(request, locals()))
        # the ajax function File() assigns this as the innerHTML of a div after the request has been completed.
        return HttpResponse(t)
        
class Questions(CoordProtectedView):
    """
        displays the questions tab
    """
    def handle_GET(self, request, **kwargs):
        path = request.META['PATH_INFO'].split('/')
        if path[3] == 'mcq':
            try:
                ques_id = path[4]
                ques = ObjectiveQuestion.objects.get(id = ques_id)
                form = AddMCQForm(instance = ques)
            except:
                form = AddMCQForm()
            template = 'ajax/events/mcq_form.html'
        elif path[3] == 'subj':
            try:
                ques_id = path[4]
                ques = SubjectiveQuestion.objects.get(id = ques_id)
                form = AddSubjectiveQuestionForm(instance = ques)
            except:
                form = AddSubjectiveQuestionForm()
            template = 'ajax/events/subj_form.html'
        else:
            event = request.user.get_profile().is_coord_of
            text_questions = event.subjectivequestion_set.all()
            mcqs = event.objectivequestion_set.all()
            template = 'ajax/events/question_tab.html'
        return render_to_response(template, locals(), context_instance = RequestContext(request))

class MobApp(CoordProtectedView):
    """
        displays the mobapp tab
    """
    def handle_GET(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        try:
            form = MobAppWriteupForm(instance = event.mobapptab)
        except:
            form = MobAppWriteupForm()
        return render_to_response('ajax/events/add_edit_mobapptab.html', locals(), context_instance = RequestContext(request))

class CustomTabs(CoordProtectedView):
    """
        displays the Custom tabs
    """
    def get_files(self, tab):
        # gets all files that are related to a particular tab
        try:
            return tab.tabfile_set.all()
        except:
            raise Http404()

    def handle_GET(self, request, **kwargs):
        path = request.META['PATH_INFO'].split('/')
        if path[3] :
            if path[3] == 'edit' :
                tab_id = path[4]
                tab = Tab.objects.get(id = tab_id)
                form = TabAddForm(instance = tab)
                template = 'ajax/events/tab_form.html'
            elif path[3] == 'files' :
                if path[4] == 'rename' :
                    tab_id = path[5]
                    file_id = path[6]
                    tab = Tab.objects.get(id = tab_id)
                    form = TabFile.objects.get(id = file_id)
                    actual_name = form.tab_file.name.split('/')[-1]
                    file_list = self.get_files(tab)
                    template = 'ajax/events/file_rename.html'
                else:
                    form = TabFileForm()
                    tab_id = path[4]
                    tab = Tab.objects.get(id = tab_id)
                    file_list = self.get_files(tab)
                    template = 'ajax/events/file_form.html'
            else:
                tab_id = path[3]
                tab = Tab.objects.get(id = tab_id)
                file_list = self.get_files(tab)
                template = 'ajax/events/tab_detail.html'
        else:
            form = TabAddForm()
            template = 'ajax/events/tab_form.html'
        return render_to_response(template, locals(), context_instance = RequestContext(request))            
    
class MCQAddEdit(CoordProtectedView):
    """
    """
    def handle_GET(self, request, **kwargs):
        mcq = None
        ques_id = kwargs['mcq_id']
        options = []
        if kwargs['mcq_id']:
            mcq = ObjectiveQuestion.objects.get(id = kwargs['mcq_id'])
            options = mcq.mcqoption_set.all()
        form = MyForm(mcq, options)
        template = 'ajax/events/mcq_form.html'
        return render_to_response(template, locals(), context_instance = RequestContext(request))
            

