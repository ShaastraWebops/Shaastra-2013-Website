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

def home(request):
    return render_to_response('controlroom/home.html', locals(),
                              context_instance=RequestContext(request))

def AddRoom(request):
    #TODO: Authenticate user is hospi coord
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
    
def individual(request):
    #TODO: Authenticate user is hospi coord
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

def team(request):
    #TODO:Authenticate user is hospi coord
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            leader = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
            check = 0
            try:
                current_team = Team.objects.get(leader = leader.user)
                check = 1
            except:
                current_team = Team.objects.filter(leader = leader.user)
            checkedin_profiles = []
            new_profiles = []
            if check == 0:
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

def TeamCheckIn(request,shaastraid = None):
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

def CheckOut(request):
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


