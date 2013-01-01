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
from datetime                   import datetime
from controlroom.generate_bill import *

@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    checkedin=IndividualCheckIn.objects.all()
    teamNameForm = TeamNameForm()
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
def AddMultipleRooms(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    form = AddMultipleRoomsForm()
    if request.method == 'POST':
        form = AddMultipleRoomsForm(request.POST, request.FILES)   
        if form.is_valid():
            line_number = 0
            rooms = [] 
            for line in form.cleaned_data['rooms']:
                line = line.replace('\n', '').replace('\r', '').replace('(','').replace(')','')
                if line == '':
                    continue
                line_number += 1
                rooms.append(line)
                try:
                    room = AvailableRooms.objects.get(room_no = line.split(',')[0])
                except:
                    room = AvailableRooms(
                                room_no = line.split(',')[0],
                                hostel =  line.split(',')[1],
                                max_number = line.split(',')[2]
                                )
                    room.save()   
                    msg = "Rooms added successfully to database"             
    return render_to_response('controlroom/AddMultipleRooms.html', locals(),
                              context_instance=RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/login/')
def RoomMap(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    alak = AvailableRooms.objects.filter(hostel='Alakananda').order_by('room_no')
    brahms = AvailableRooms.objects.filter(hostel='Brahmaputra').order_by('room_no')
    cauvery = AvailableRooms.objects.filter(hostel='Cauvery').order_by('room_no')
    ganga = AvailableRooms.objects.filter(hostel='Ganga').order_by('room_no')
    godav = AvailableRooms.objects.filter(hostel='Godavari').order_by('room_no')
    jam = AvailableRooms.objects.filter(hostel='Jamuna').order_by('room_no')
    krishna = AvailableRooms.objects.filter(hostel='Krishna').order_by('room_no')
    mahanadhi = AvailableRooms.objects.filter(hostel='Mahanadhi').order_by('room_no')
    mandak = AvailableRooms.objects.filter(hostel='Mandakini').order_by('room_no')
    narmad = AvailableRooms.objects.filter(hostel='Narmada').order_by('room_no')
    pamba = AvailableRooms.objects.filter(hostel='Pamba').order_by('room_no')
    saras = AvailableRooms.objects.filter(hostel='Saraswathi').order_by('room_no')
    sarayu = AvailableRooms.objects.filter(hostel='Sarayu').order_by('room_no')
    sharav = AvailableRooms.objects.filter(hostel='Sharavati').order_by('room_no')
    sindhu = AvailableRooms.objects.filter(hostel='Sindhu').order_by('room_no')
    tambi = AvailableRooms.objects.filter(hostel='Tamraparani').order_by('room_no')
    tapti = AvailableRooms.objects.filter(hostel='Tapti').order_by('room_no')
    return render_to_response('controlroom/RoomMap.html', locals(),
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
            if inputs['shaastraID']:
                participant = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
            else:
                usr = User.objects.get(email = inputs['email'])
                participant = UserProfile.objects.get(user = usr)
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=participant.shaastra_id)
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
    rooms = AvailableRooms.objects.filter(already_checkedin__lt=F('max_number')).order_by('hostel')
    hostels = HOSTEL_CHOICES
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            try:
                try:
                    leader = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
                except:
                    usr = User.objects.get(email = inputs['email'])
                    leader = UserProfile.objects.get(user = usr)
            except:
                msg = "This participant does not exist"
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
            if inputs['shaastraID']:
                participant = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
            else:
                usr = User.objects.get(email = inputs['email'])
                participant = UserProfile.objects.get(user = usr)
            s_id = participant.shaastra_id
            checkedin = IndividualCheckIn.objects.get(shaastra_ID=s_id)
            print s_id
            try:
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=s_id)
                if checkedin.check_out_date:
                    msg = "This participant is already checked-out!"
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
                else:
                    values = {'check_out_date': datetime.now,'check_out_control_room':checkedin.check_in_control_room}
                    individual_form = IndividualForm(instance=checkedin,initial=values)
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

def Register(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    values = {'want_accomodation':True}
    form = UserForm(initial=values)
    if request.method == 'POST':
        values = {'want_accomodation':True}
        form = UserForm(request.POST,initial=values)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],
                            last_name=data['last_name'],
                            username=data['username'], email=data['email'])
            new_user.set_password(data['password'])
            new_user.is_active = True
            new_user.save()
            x = 1300000 + new_user.id   
            shaastra_id = ("SHA" + str(x))
            userprofile = UserProfile(
                user=new_user,
                gender=data['gender'],
                age=data['age'],
                branch=data['branch'],
                mobile_number=data['mobile_number'],
                college=data['college'],
                college_roll=data['college_roll'],
                shaastra_id= ("SHA" + str(x)),
                )
            userprofile.save()
            msg = "Your Shaastra ID is " + shaastra_id
    return render_to_response('controlroom/register.html', locals(),
                              context_instance=RequestContext(request))
                              
@login_required
def CreateTeam(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    
    form = CreateTeamForm()
    
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            leader = UserProfile.objects.get(shaastra_id = form.cleaned_data['leader_shaastra_ID']).user
            try:
                Team.objects.get(members__pk = leader.id, event = form.cleaned_data['event'])
                return render_to_response('users/teams/already_part_of_a_team.html', locals(), context_instance = RequestContext(request))
            except Team.DoesNotExist:
                pass
            team = form.save(commit = False)
            team.leader = leader
            '''
            try:
                team.leader.get_profile().registered.get(pk = team.event.id)
            except Event.DoesNotExist:
                team.leader.get_profile().registered.add(team.event)
            '''
            team.save()
            team.members.add(leader)
            return HttpResponseRedirect('%suser/teams/%s/' % (settings.SITE_URL, team.id))
    return render_to_response('users/teams/create_team.html', locals(), context_instance = RequestContext(request))

@login_required
def EditTeam(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
        
    form = TeamNameForm()
    
    if request.method == 'POST':
        form = TeamNameForm(request.POST)
        if form.is_valid():
            try:
                team = Team.objects.get(name = form.cleaned_data['team_name'])
            except:
                raise Http404('Team not found.')
            return HttpResponseRedirect('%suser/teams/%s/' % (settings.SITE_URL, team.id))
    
    return HttpResponseRedirect('%scontrolroom/home/' % settings.SITE_URL)
        
def GenerateBill(request,pk):
    profile = UserProfile.objects.get(id = pk)
    s_id = profile.shaastra_id
    pdf = generateParticipantPDF(s_id)
    return HttpResponse(pdf)    

