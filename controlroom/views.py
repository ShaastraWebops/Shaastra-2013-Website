#!/usr/bin/python
# -*- coding: utf-8 -*-
import django
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from events.models import *
from users.models import *
from controlroom.models import *
from django.utils.translation import ugettext as _
from controlroom.forms import *
from django.contrib.sessions.models import Session
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.mail import send_mail as mailsender
from recaptcha.client import captcha
import sha
import random
import datetime

@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    checkedin=IndividualCheckIn.objects.all()
    return render_to_response('controlroom/home.html', locals(),
                              context_instance=RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def AddRoom(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid:
            form.save()
            msg = "Room Added"
            return render_to_response('controlroom/AddRoomForm.html', locals(),
                              context_instance=RequestContext(request))
        else:
            msg="Invalid Form"
            return render_to_response('controlroom/AddRoomForm.html', locals(),
                              context_instance=RequestContext(request))
    else:
        form = AddRoomForm()
        return render_to_response('controlroom/AddRoomForm.html', locals(),
                              context_instance=RequestContext(request))
    
@login_required(login_url=settings.SITE_URL + 'user/login/')
def individual(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    msg = "Enter Shaastra ID of participant"
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            participant = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=inputs['shaastraID'])
                msg = "This participant is already checked-in!"
                return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
            except:
                individual_form = IndividualForm(initial = {'shaastra_ID' : participant.shaastra_id, 'first_name' : participant.user.first_name, 'last_name' : participant.user.last_name, 'phone_no' : participant.mobile_number, })
                return render_to_response('controlroom/individual.html', locals(),
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
    else:
        form = ShaastraIDForm()
        return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def team(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    msg = "Enter Shaastra ID of Team leader"
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            try:
                leader = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
            except:
                msg = "This shaastra ID does not exist"
                return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
            check = 0
            try:
                current_team = Team.objects.get(leader = leader.user)
                check = 1
            except:
                current_team = Team.objects.filter(leader = leader.user)
                check = 2
            if not current_team:
                msg = "This person is not a team leader"
                return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
            checkedin_profiles = []
            new_profiles = []
            if check == 2:
                for t in current_team:
                    for m in t.members.all():
                        profile = UserProfile.objects.get(user = m)
                        try:
                            checkedin = IndividualCheckIn.objects.get(shaastra_ID=profile.shaastra_id)
                            checkedin_profiles.append(checkedin)
                        except:
                            new_profiles.append(profile)
            else:
                for m in current_team.members.all():
                        profile = UserProfile.objects.get(user = m)
                        try:
                            checkedin = IndividualCheckIn.objects.get(shaastra_ID=profile.shaastra_id)
                            checkedin_profiles.append(checkedin)
                        except:
                            new_profiles.append(profile)    
            return render_to_response('controlroom/team.html', locals(),
                                  context_instance=RequestContext(request))
        else:
            return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
    else:
        form = ShaastraIDForm()
        return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def TeamCheckIn(request,shaastraid = None):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    participant = UserProfile.objects.get(shaastra_id=shaastraid)
    try:
        checkedin = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
        msg = "This participant is already checked-in!"
        return render_to_response('controlroom/shaastraIDform.html', locals(),
                      context_instance=RequestContext(request)) 
    except:
        individual_form = IndividualForm(initial = {'shaastra_ID' : participant.shaastra_id, 'first_name' : participant.user.first_name, 'last_name' : participant.user.last_name, 'phone_no' : participant.mobile_number, })
        return render_to_response('controlroom/individual.html', locals(),
                              context_instance=RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def CheckOut(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            participant = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=inputs['shaastraID'])
                if checkedin.check_out_date:
                    msg = "This participant is already checked-out!"
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
                else:
                    individual_form = IndividualForm(instance=checkedin)
                    return render_to_response('controlroom/individual.html', locals(),
                                          context_instance=RequestContext(request))
            except:
                msg = "This participant never checked-in!"
                return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
        else:
            return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
    else:
        form = ShaastraIDForm()
        return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request))


