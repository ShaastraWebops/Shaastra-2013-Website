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
from controlroom.generate_bill import *

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
    r = form['room']
    rm = AvailableRooms.objects.get(id=r)
    check_in = form['checkin']
    comments = form['comments'] 
    msg = " "
    try:
        for s_id in form['sub_checklist']:
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID = s_id)
                msg = msg + s_id + ','
            except:
                profile = UserProfile.objects.get(shaastra_id = s_id)
                new_guest = IndividualCheckIn(room = rm,
                                              shaastra_ID = profile.shaastra_id,
                                              first_name = profile.user.first_name,
                                              last_name = profile.user.last_name,
                                              phone_no = profile.mobile_number,
                                              check_in_control_room = check_in,
                                              comments = comments,
                                              )
                new_guest.save()
                room = AvailableRooms.objects.get(id = rm)
                room.already_checkedin = room.already_checkedin + 1
                room.save()
        if msg == " ":
            msg = "All members checked in successfully!"
        else:
            msg = msg + " already checked in"
    except:
        s_id = form['sub_checklist']
        try:
            checkedin = IndividualCheckIn.objects.get(shaastra_ID = s_id)
            msg = s_id + " is already checked in"
        except:
            profile = UserProfile.objects.get(shaastra_id = s_id)
            new_guest = IndividualCheckIn(room = rm,
                                          shaastra_ID = profile.shaastra_id,
                                          first_name = profile.user.first_name,
                                          last_name = profile.user.last_name,
                                          phone_no = profile.mobile_number,
                                          check_in_control_room = check_in,
                                          comments = comments,
                                          )
            new_guest.save()
            room = AvailableRooms.objects.get(id = r)
            room.already_checkedin = room.already_checkedin + 1
            room.save()
            msg = "Checked In successfully!"
    print msg
    dajax.alert(msg)
    return dajax.json


