#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from dajax.core import Dajax
from django.utils import simplejson
from django.template import loader, Context, RequestContext, Template
from users.models import UserProfile
from controlroom.models import *
from controlroom.forms import *
from dajaxice.decorators import dajaxice_register
from django.core.cache import cache
from django.contrib.sitemaps import ping_google
from operator import attrgetter
from datetime import datetime

@dajaxice_register
def save_individual_checkin(request,form):
    dajax =Dajax()
    individual_form=IndividualForm(form)
    if individual_form.is_valid():
        form = individual_form.save()
        room = AvailableRooms.objects.get(id = form.room_id)
        room.already_checkedin = room.already_checkedin + 1
        room.save()
        msg = "Checked In Successfully!"
        dajax.alert(msg)
    else:
        msg = "Invalid Form" 
        dajax.alert(msg)
    return dajax.json()

@dajaxice_register
def save_individual_checkout(request,form,shaastraid):
    dajax =Dajax()
    checkedin = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
    individual_form=IndividualForm(form, instance = checkedin)
    if individual_form.is_valid():
        form = individual_form.save()
        room = AvailableRooms.objects.get(id = form.room_id)
        room.already_checkedin = room.already_checkedin - 1
        room.save()
        msg = "Checked Out Successfully!"
        dajax.alert(msg)
    else:
        msg = "Invalid Form" 
        dajax.alert(msg)
    return dajax.json()

@dajaxice_register
def send_participants(request,form):
    dajax = Dajax()
    try:
        for s_id in form['sub_checklist']:
            profile = UserProfile.objects.get(shaastra_id = s_id)
            rm = form['room']
            new_guest = IndividualCheckIn(room__id = rm,
                                          shaastra_ID = s_id,
                                          first_name = profile.user.first_name,
                                          last_name = profile.user.last_name,
                                          phone_no = profile.mobile_number,
                                          check_in_control_room = form['checkin'],
                                          comments = form['comments'],
                                          )
            new_guest.save()
            room = AvailableRooms.objects.get(id = rm)
            room.already_checkedin = room.already_checkedin + 1
            room.save()
            msg = "Checked In successfully!"
    except:
        s_id = form['sub_checklist']
        profile = UserProfile.objects.get(shaastra_id = s_id)
        rm = form['room']
        #new = IndividualCheckIn.objects.get(check_in_control_room = form['checkin'])
        #print rm
        #print new.shaastra_ID
        #print "Hello"
        new = IndividualCheckIn(room__id=rm, shaastra_ID=s_id, first_name=profile.user.first_name, last_name=profile.user.last_name,     phone_no=profile.mobile_number, check_in_control_room=form['checkin'], comments = form['comments'] )
        #print "Hello"
        new.save()
        print "Hello"
        room = AvailableRooms.objects.get(id = rm)
        room.already_checkedin = room.already_checkedin + 1
        room.save()
        msg = "Checked In successfully!"
    dajax.alert(msg)
    return dajax.json
