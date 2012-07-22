from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.conf import settings
from core.forms import *
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    """
        This is the home page view of the core
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('core/home.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
@csrf_exempt
def addevent(request):
    """
        This is the home page view of the superuser
    """
    if request.user.get_profile().is_core is False and not request.user.get_profile().is_coord_of :
        return HttpResponseRedirect(settings.SITE_URL)
    if(request.method=='POST'):
        filename = request.META['HTTP_X_FILE_NAME']
        event_id = request.META['HTTP_X_EVENT_ID']

        direc = os.path.join('/home/shaastra/public_html/2013/media/events',event_id)
        # note that event and tab IDs and not their titles have been used to create folders so that renaming does not affect the folders
        if not os.path.exists(direc):
            os.makedirs(direc)
        path = os.path.join(direc, filename)
        event = Event.objects.get(id = event_id)
        event.events_logo = '/2013/media'+path.split('/media')[1]
        event.save()
        # get_or_create returns a tuple whose second element is a boolean which is True if it is creating a new object.
        # the first element is the object that has been created/found.
        f = open(path, 'w')
        with f as dest:
            req = request
            # Right now the file comes as raw input (in form of binary strings). Unfortunately, this is the only way I know that will make ajax work with file uploads.
            foo = req.read( 1024 )
            while foo:
                dest.write( foo )
                foo = req.read( 1024 )
        html= "<p>Event Name : "+ str(event)+"<br>Category   :"+ event.category +"<br></p>"
        return HttpResponse(html)
    else:
        event_form=AddEventForm()
    return render_to_response('ajax/core/addevent.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def eventdashboard(request,id=0):
    """
        This is the home page view of the superuser
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    profile = request.user.get_profile()
    profile.is_coord_of = Event.objects.get(id = id)
    profile.save()
    return HttpResponseRedirect(settings.SITE_URL+'coord/')

@login_required(login_url=settings.SITE_URL + 'user/login/')
def editevent(request,id=0):
    """
        This is the home page view of the superuser
    """
#    if request.user.get_profile().is_core is False :
#        return HttpResponseRedirect(settings.SITE_URL)
    event_form=AddEventForm(instance=Event.objects.get(id=id))
    return render_to_response('ajax/core/editevent.html', locals(), context_instance = RequestContext(request))
    

