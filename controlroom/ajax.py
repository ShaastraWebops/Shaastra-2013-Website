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
    try:
        checkedin = IndividualCheckIn.objects.get(shaastra_ID = form['shaastra_ID'])
        rm = checkedin.room
        individual_form=IndividualForm(form,croom=checkedin.room,instance=checkedin)
        if individual_form.is_valid():
            form1 = individual_form.save(commit=False)
            form1.check_out_date = None
            rm.already_checkedin = rm.already_checkedin - 1
            rm.mattresses = rm.mattresses - checkedin.number_of_mattresses_given 
            rm.save()
            room = AvailableRooms.objects.get(id = form1.room_id)
            room.already_checkedin = room.already_checkedin + 1
            room.mattresses = room.mattresses + form1.number_of_mattresses_given 
            room.save()
            form1.save()
            msg = "Updated Successfully!"
        else:
            msg = "Invalid Form1"
    except:
        individual_form=IndividualForm(form)
        if individual_form.is_valid():
            form1 = individual_form.save(commit=False)
            form1.check_out_date = None
            room = AvailableRooms.objects.get(id = form1.room_id)
            room.already_checkedin = room.already_checkedin + 1
            room.mattresses = room.mattresses + form1.number_of_mattresses_given
            room.save()
            form1.save()
            msg = "Checked In Successfully!"
        else:
            msg = "Invalid Form"            
    dajax.alert(msg)
    dajax.script("$('#checkin_button').show();")
    return dajax.json()
'''
@dajaxice_register
def save_individual_checkin(request,form):
    dajax =Dajax()
    individual_form=IndividualForm(form)
    if individual_form.is_valid():
        checkedin = IndividualCheckIn(shaastra_id = individual_form.shaastra_id)
        form = individual_form.save()
        room = AvailableRooms.objects.get(id = form.room_id)
        room.already_checkedin = room.already_checkedin + 1
        room.mattresses = room.mattresses + form.number_of_mattresses_given
        room.save()
        msg = "Checked In Successfully!"
        dajax.alert(msg)
        form = individual_form.save(commit = False)
        #form.check_out_date = 'NULL'
        try:
            checkedin = IndividualCheckIn.objects.get(shaastra_ID = form.shaastra_ID)
            form.save()
            room = AvailableRooms.objects.get(id = form.room_id)
            room.mattresses = room.mattresses + form.number_of_mattresses_given - checkedin.number_of_mattresses_given
            room.save()
            msg = "Updated Successfully!"
        except:
            form.save()
            room = AvailableRooms.objects.get(id = form.room_id)
            room.already_checkedin = room.already_checkedin + 1
            room.mattresses = room.mattresses + form.number_of_mattresses_given
            room.save()
            msg = "Checked In Successfully!"
         
    else:
        msg = "Invalid Form" 
    dajax.alert(msg)
    return dajax.json()
'''
@dajaxice_register
def save_individual_checkout(request,form,shaastraid):
    dajax =Dajax()
    checkedin = IndividualCheckIn.objects.get(shaastra_ID=shaastraid)
    individual_form=IndividualForm(form, instance = checkedin)
    if individual_form.is_valid():
        form = individual_form.save(commit=False)
        form.check_out_date = datetime.now()
        form.save()
        room = AvailableRooms.objects.get(id = form.room_id)
        room.already_checkedin = room.already_checkedin - 1
        room.mattresses = room.mattresses + form.number_of_mattresses_given
        room.save()
        msg = "Checked Out Successfully!"
        dajax.alert(msg)
    else:
        msg = "Invalid Form" 
        dajax.alert(msg)
    return dajax.json()

@dajaxice_register
def send_participants(request,form,uid):
    dajax = Dajax()
    r = form['room']
    rm = AvailableRooms.objects.get(id=r)
    leader = UserProfile.objects.get(id = uid)
    check_in = form['checkin']
    comments = form['comments'] 
    duration = form['no_of_days']
    mattresses = form['mattresses']
    s_ids = form['sub_checklist']
    if not isinstance(s_ids, list):
        s_ids = [s_ids]
    msg = " "
    room = AvailableRooms.objects.get(id = r)

    for s_id in s_ids:
        try:
            checkedin = IndividualCheckIn.objects.get(shaastra_ID = s_id)
            msg = msg + s_id + ','
        except:
            profile = UserProfile.objects.get(shaastra_id = s_id)
            new_guest = IndividualCheckIn(room = rm,
                                          gender = profile.gender,
                                          duration_of_stay=duration,
                                          mattress_room = form['mattroom'],
                                          shaastra_ID = profile.shaastra_id,
                                          first_name = profile.user.first_name,
                                          last_name = profile.user.last_name,
                                          phone_no = profile.mobile_number,
                                          check_in_control_room = check_in,
                                          comments = comments,
                                          )
            new_guest.save()
            room.already_checkedin = room.already_checkedin + 1
    if room:
        room.mattresses = room.mattresses + int(mattresses)
        room.save()
    try:
        matt = Mattresses.objects.get(team_leader_id = leader.shaastra_id)
        matt.no_of_mattresses = matt.no_of_mattresses + int(mattresses)
        matt.save()
    except:
        matt = Mattresses(team_leader_id = leader.shaastra_id,
                          no_of_mattresses = int(mattresses))
        matt.save()
    if msg == " ":
        msg = "All members checked in successfully!"
    else:
        msg = msg + " already checked in"
    dajax.alert(msg)
    #dajax.assign('#allot_room_button','disabled',false)
    return dajax.json()
