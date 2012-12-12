#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.conf import settings
from admin.forms import *
from django.contrib.auth.models import Group


@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    """
        This is the home page view of the superuser
    """

    if request.user.is_superuser is False:
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('admin/home.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/login/')
def addgroup(request):
    """
        This is the home page view of the superuser
    """

    if request.user.is_superuser is False:
        return HttpResponseRedirect(settings.SITE_URL)
    group_form = AddGroupForm()
    return render_to_response('ajax/admin/addgroup.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/login/')
def editgroup(request, id=0):
    """
        This is the home page view of the superuser
    """

    if request.user.is_superuser is False:
        return HttpResponseRedirect(settings.SITE_URL)
    group_form = AddGroupForm(instance=Group.objects.get(id=id))
    return render_to_response('ajax/admin/editgroup.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/login/')
def addcore(request):
    """
        This is the home page view of the superuser
    """

    if request.user.is_superuser is False:
        return HttpResponseRedirect(settings.SITE_URL)
    core_form = AddCoreForm()
    return render_to_response('ajax/admin/addcore.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/login/')
def editcore(request, id=0):
    """
        This is the home page view of the superuser
    """

    if request.user.is_superuser is False:
        return HttpResponseRedirect(settings.SITE_URL)
    core_form = AddCoreForm(instance=User.objects.get(id=id),
                            initial={'groups': User.objects.get(id=id).groups.get_query_set()[0]})
    return render_to_response('ajax/admin/editcore.html', locals(),
                              context_instance=RequestContext(request))

