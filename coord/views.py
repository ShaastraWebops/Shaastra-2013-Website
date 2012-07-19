from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from events.models import *
from coord.forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

import os
import datetime
from datetime import date

# Create your views here.

class BaseView(object):
    # parent class. classes below inherit this
    def __call__(self, request, **kwargs):
        # handles request and dispatches the corresponding handler based on the type of request (GET/POST)
        if not self.authenticate_req(request): return HttpResponseRedirect(settings.SITE_URL+'user/login')
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
            raise Http404()
    
    def authenticate_req(self, req):
        try:
            eve = req.user.get_profile().is_coord_of
        except:
            return False
        return True
            
class CoordDashboard(BaseView):
    """
    displays the coord dashboard depending on the logged in coords event
    """
    def handle_GET(self, request, **kwargs):
        update = Update.objects.all()
        event = request.user.get_profile().is_coord_of
        tabs = self.get_tabs(event)
        return render_to_response('coord/dashboard.html', locals(), context_instance = RequestContext(request))
        
class TabFileSubmit(BaseView):
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
        direc = os.path.join('/home/shaastra/public_html/2013/media', 'events', str(tab.event.id), tab._meta.object_name, str(tab.id))
        # note that event and tab IDs and not their titles have been used to create folders so that renaming does not affect the folders
        if not os.path.exists(direc):
            os.makedirs(direc)
        path = os.path.join(direc, filename)
        a = TabFile.objects.get_or_create(tab_file = path)
        # get_or_create returns a tuple whose second element is a boolean which is True if it is creating a new object.
        # the first element is the object that has been created/found.
        if a[1]:
            a[0].url = os.path.join('/2013/media', 'events', str(tab.event.id), tab._meta.object_name, str(tab.id), filename)
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

        template = loader.get_template('ajax/coord/file_list.html')
        t = template.render(RequestContext(request, locals()))
        # the ajax function File() assigns this as the innerHTML of a div after the request has been completed.
        return HttpResponse(t)

def get_objective(ques_id):
    try:
        return ObjectiveQuestion.objects.get(id = ques_id)
    except:
        return None
        
def get_options(mcq):
    try:
        return mcq.mcqoption_set.all()
    except:
        return []
        
class Questions(BaseView):
    """
        displays the questions tab
    """
    def handle_GET(self, request, **kwargs):
        path = request.META['PATH_INFO'].split('/')
        if path[3] == 'mcq':
            try:
                ques_id = path[4]
            except:
                ques_id = 0
            mcq = get_objective(ques_id)
            options = get_options(mcq)
            form = MCQForm(mcq, options)
            template = 'ajax/coord/mcq_form.html'
        elif path[3] == 'subj':
            try:
                ques_id = path[4]
                ques = SubjectiveQuestion.objects.get(id = ques_id)
                form = AddSubjectiveQuestionForm(instance = ques)
            except:
                form = AddSubjectiveQuestionForm()
            template = 'ajax/coord/subj_form.html'
        else:
            event = request.user.get_profile().is_coord_of
            text_questions = event.subjectivequestion_set.all()
            mcqs = event.objectivequestion_set.all()
            template = 'ajax/coord/question_tab.html'
        return render_to_response(template, locals(), context_instance = RequestContext(request))

class MobApp(BaseView):
    """
        displays the mobapp tab
    """
    def handle_GET(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        try:
            form = MobAppWriteupForm(instance = event.mobapptab)
        except:
            form = MobAppWriteupForm()
        return render_to_response('ajax/coord/add_edit_mobapptab.html', locals(), context_instance = RequestContext(request))

class CustomTabs(BaseView):
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
                template = 'ajax/coord/tab_form.html'
            elif path[3] == 'files' :
                if path[4] == 'rename' :
                    tab_id = path[5]
                    file_id = path[6]
                    tab = Tab.objects.get(id = tab_id)
                    form = TabFile.objects.get(id = file_id)
                    actual_name = form.tab_file.name.split('/')[-1]
                    file_list = self.get_files(tab)
                    template = 'ajax/coord/file_rename.html'
                else:
                    form = TabFileForm()
                    tab_id = path[4]
                    tab = Tab.objects.get(id = tab_id)
                    file_list = self.get_files(tab)
                    template = 'ajax/coord/file_form.html'
            else:
                tab_id = path[3]
                tab = Tab.objects.get(id = tab_id)
                file_list = self.get_files(tab)
                template = 'ajax/coord/tab_detail.html'
        else:
            form = TabAddForm()
            template = 'ajax/coord/tab_form.html'
        return render_to_response(template, locals(), context_instance = RequestContext(request))

class MCQAddEdit(BaseView):
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
        template = 'ajax/coord/mcq_form.html'
        return render_to_response(template, locals(), context_instance = RequestContext(request))

def AddUpdate(request):
    """
    """
#    return HttpResponse("blah")
    update_form=UpdateForm()
    template = 'ajax/coord/update.html'
    return render_to_response(template, locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def EditUpdate(request,id=0):
    """
        
    """
    update_form=UpdateForm(instance=Update.objects.get(id=id))
    return render_to_response('ajax/coord/editupdate.html', locals(), context_instance = RequestContext(request))
