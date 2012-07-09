from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.conf import settings
from core.forms import *

@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    """
        This is the home page view of the core
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('core/home.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def addevent(request):
    """
        This is the home page view of the superuser
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    event_form=AddEventForm()
    return render_to_response('ajax/core/addevent.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def editevent(request,id=0):
    """
        This is the home page view of the superuser
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    event_form=AddEventForm(instance=Event.objects.get(id=id))
    return render_to_response('ajax/core/editevent.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def addcoord(request):
    """
        This is the home page view of the superuser
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    coord_form=AddCoordForm()
    return render_to_response('ajax/core/addcoord.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def editcoord(request,id=0):
    """
        This is the home page view of the superuser
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    coord=User.objects.get(id=id)
    coord_form = AddCoordForm(instance=coord,initial={'event':coord.get_profile().is_coord_of,})
    return render_to_response('ajax/core/editcoord.html', locals(), context_instance = RequestContext(request))