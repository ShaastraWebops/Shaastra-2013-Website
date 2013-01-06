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
from datetime import datetime
from controlroom.generate_bill import *
from prizes.models import BarcodeMap, Participant
from users.forms import EditUserForm

@login_required
def home(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    checkedin=IndividualCheckIn.objects.all()
    teamNameForm = TeamNameForm()
    return render_to_response('controlroom/home.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def AddRoom(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    if request.method == 'POST':
        form = AddRoomForm(request.POST)
        if form.is_valid:
            form.save()
            msg = "Room Added"
            return render_to_response('controlroom/home.html', locals(),
                              context_instance=RequestContext(request))
        else:
            msg="Invalid Form"
            return render_to_response('controlroom/AddRoomForm.html', locals(),
                              context_instance=RequestContext(request))
    else:
        form = AddRoomForm()
        return render_to_response('controlroom/AddRoomForm.html', locals(),
                              context_instance=RequestContext(request))

@login_required
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
                    room = AvailableRooms.objects.get(room_no = line.split(',')[0],hostel =  line.split(',')[1])
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

@login_required
def RoomMap(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    alak = AvailableRooms.objects.filter(hostel='Alakananda').order_by('room_no')
    ganga = AvailableRooms.objects.filter(hostel='Ganga').order_by('room_no')
    jam = AvailableRooms.objects.filter(hostel='Jamuna').order_by('room_no')
    mahanadhi = AvailableRooms.objects.filter(hostel='Mahanadhi').order_by('room_no')
    mandak = AvailableRooms.objects.filter(hostel='Mandakini').order_by('room_no')
    pamba = AvailableRooms.objects.filter(hostel='Pamba').order_by('room_no')
    sarayu = AvailableRooms.objects.filter(hostel='Sarayu').order_by('room_no')
    sharav = AvailableRooms.objects.filter(hostel='Sharavati').order_by('room_no')
    sindhu = AvailableRooms.objects.filter(hostel='Sindhu').order_by('room_no')
    tambi = AvailableRooms.objects.filter(hostel='Tamraparani').order_by('room_no')
    sarayu_extn = AvailableRooms.objects.filter(hostel='Sarayu Extn').order_by('room_no')
    c28 = AvailableRooms.objects.filter(hostel='C-2-8').order_by('room_no')
    return render_to_response('controlroom/RoomMap.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def individual(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    msg = "Enter Shaastra ID of participant"
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            if inputs['shaastraID']:
                try:
                    participant = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
                except:
                    msg = "The entered Shaastra ID does not exist."
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                                      context_instance=RequestContext(request))
            elif inputs['barcode']:
                try:
                    barcode = BarcodeMap.objects.using('erp').get(barcode=inputs['barcode'])
                    shaastra_id = barcode.shaastra_id
                    participant = UserProfile.objects.get(shaastra_id=shaastra_id)
                except:
                    msg = "The entered barcode does not correspond to an existing shaastra ID."
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                                      context_instance=RequestContext(request))
            else:
                try:
                    usr = User.objects.get(email = inputs['email'])
                    participant = UserProfile.objects.get(user = usr)
                except:
                    msg = "The entered email ID does not correspond to an existing user."
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                                      context_instance=RequestContext(request))
            college = participant.college
            try:
                #msg = "1"
                checkedin = IndividualCheckIn.objects.get(shaastra_ID=participant.shaastra_id)
                #msg = msg + "2"
                #values = {'room':checkedin.room,}
                individual_form = IndividualForm(croom=checkedin.room,instance = checkedin)
                #msg = msg + "3"
                msg = "This participant is already checked-in into " + str(checkedin.room)
                checkintime = checkedin.check_in_date
                checkouttime = checkedin.check_out_date
                if checkouttime:
                    msg = "This participant was checked-in into " + str(checkedin.room) + ". He has checked-out!"
                return render_to_response('controlroom/individual.html', locals(),
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

@login_required
def team(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    msg = "Enter Shaastra ID of Team leader"
    rooms = AvailableRooms.objects.filter(already_checkedin__lt=F('max_number')).order_by('hostel').order_by('room_no')
    checkin = CONTROL_ROOM_CHOICES
    matt = MATTRESS_CHOICES
    if request.method == 'POST':
        form = ShaastraIDForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            if inputs['shaastraID']:
                try:
                    leader = UserProfile.objects.get(shaastra_id=inputs['shaastraID'])
                except:
                    msg = "This participant does not exist"
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request)) 
            elif inputs['barcode']:
                try:
                    barcode = BarcodeMap.objects.using('erp').get(barcode=inputs['barcode'])
                    shaastra_id = barcode.shaastra_id
                    leader = UserProfile.objects.get(shaastra_id=shaastra_id)
                except:
                    msg = "The entered barcode does not correspond to an existing shaastra ID."
                    return render_to_response('controlroom/shaastraIDform.html', locals(),
                                      context_instance=RequestContext(request))
            else:
                try:
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
                            if not checkedin in checkedin_profiles:
                                checkedin_profiles.append(checkedin)
                        except:
                            if not profile in new_profiles:
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

@login_required
def IdForBill(request):
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
                            if not checkedin in checkedin_profiles:
                                checkedin_profiles.append(checkedin)
                        except:
                            if not profile in new_profiles:
                                new_profiles.append(profile)
            else:
                for m in current_team.members.all():
                        profile = UserProfile.objects.get(user = m)
                        try:
                            checkedin = IndividualCheckIn.objects.get(shaastra_ID=profile.shaastra_id)
                            checkedin_profiles.append(checkedin)
                        except:
                            new_profiles.append(profile)
            return render_to_response('controlroom/idforbill.html', locals(),
                                  context_instance=RequestContext(request))
        else:
            return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request))
    else:
        form = ShaastraIDForm()
        return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request))    
@login_required
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

@login_required
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
                    values = {'check_out_date': datetime.now(),'check_out_control_room':checkedin.check_in_control_room}
                    print datetime.now()
                    individual_form = IndividualForm(initial=values,instance=checkedin)
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

@login_required
def Register(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],
                            last_name=data['last_name'],
                            username=data['username'], email=data['email'])
            new_user.set_password('default')
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
                want_accomodation = True,
                )
            userprofile.save()
            p = Participant(
                name=new_user.username,
                gender=data['gender'],
                age=data['age'],
                branch=data['branch'],
                mobile_number=data['mobile_number'],
                college=new_user.get_profile().college,
                college_roll=data['college_roll'],
                shaastra_id= ("SHA" + str(x)),
                )
            p.save(using='erp')
            msg = "Your Shaastra ID is " + shaastra_id
    return render_to_response('controlroom/register.html', locals(),
                              context_instance=RequestContext(request))
                              
@login_required
def CreateTeam(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    event = Event.objects.get(title='hospi')
    form = CreateTeamForm(initial={'event':event})
    
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            leader = UserProfile.objects.get(shaastra_id = form.cleaned_data['leader_shaastra_ID']).user
            try:
                Team.objects.get(members__pk = leader.id, event = event)
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

@login_required        
def GenerateBill(request,pk):
    profile = UserProfile.objects.get(id = pk)
    s_id = profile.shaastra_id    
#    if int(team) == 0:
    pdf = generateParticipantPDF(s_id,0)
    return pdf
#    else:
#        form = TeamBillForm()
#        if request.method == 'POST':
#            form = TeamBillForm(request.POST)
#            if form.is_valid():
#                pdf = generateParticipantPDF(s_id,team,form.cleaned_data['number_of_participants'])
#                return pdf  
#        return render_to_response('controlroom/shaastraIDform.html', locals(),
#                              context_instance=RequestContext(request))

@login_required        
def TeamGenerateBill(request):  
    if request.method == 'POST':
        profile = UserProfile.objects.get(id = request.POST['leader_id'])
        s_id = profile.shaastra_id  
#        count = 0
#        for s_id in request.POST['sub_checklist']
#            count  = count +1
#        assert False
        a = []
        for m in range(1,int(request.POST['counter'])+1):
            try:
                name = 'sub_checklist'+str(m)
                a.append(request.POST[name])
            except:
                pass
        pdf = generateParticipantPDF(s_id,1,a)
        return pdf 
    return render_to_response('controlroom/shaastraIDform.html', locals(),
                              context_instance=RequestContext(request))    
  
@login_required
def RoomDetails(request,id):
    room = AvailableRooms.objects.get(id = id)
    try:
        checkedin = IndividualCheckIn.objects.filter(room = room)
    except:
        msg = "Room is currently empty!"
    return render_to_response('controlroom/RoomDetails.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def EditProfile(request):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    
    if request.method == 'POST':
        shaastraid = request.POST['shaastra_id']
        barcode = request.POST['barcode']
        if barcode :
            try:
                barcode_obj = BarcodeMap.objects.using('erp').get(barcode=barcode)
                shaastraid = barcode_obj.shaastra_id
                return HttpResponseRedirect('%scontrolroom/edituserprofile/%s' % (settings.SITE_URL,shaastraid))
            except:
                msg = "Please enter a valid Shaastra ID or Barcode."
            return render_to_response('controlroom/home.html', locals(),
                              context_instance=RequestContext(request))
        elif shaastraid:
            return HttpResponseRedirect('%scontrolroom/edituserprofile/%s' % (settings.SITE_URL,shaastraid))
        else:
            msg = "Please enter a valid Shaastra ID or Barcode."
            return render_to_response('controlroom/home.html', locals(),
                              context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('%scontrolroom/home/' % settings.SITE_URL)

@login_required
def EditUserProfile(request,shaastraid):
    if request.user.get_profile().is_hospi is False:
        return HttpResponseRedirect(settings.SITE_URL)
    
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(shaastra_id = shaastraid)
        user = userprofile.user
        editProfileForm = EditUserForm(request.POST, instance = userprofile)
        if editProfileForm.is_valid():
            profile = editProfileForm.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            #new_user = User.objects.using('erp').get(username=user.username)
            #new_user.first_name = user.first_name
            #new_user.last_name = user.last_name
            #new_user.save()
            p = Participant.objects.using('erp').get(shaastra_id = user.get_profile().shaastra_id)
            p.name=user.username
            p.gender=profile.gender
            p.age=profile.age
            p.branch=profile.branch
            p.mobile_number=profile.mobile_number
            p.college=str(user.get_profile().college),
            p.college_roll=profile.college_roll
            p.shaastra_id= profile.shaastra_id
            p.save()
            return HttpResponseRedirect('%scontrolroom/home/' % settings.SITE_URL)
        else:
            return render_to_response('users/edit_profile.html', locals(),context_instance=RequestContext(request))
    else:
        userprofile = UserProfile.objects.get(shaastra_id = shaastraid)
        user = userprofile.user
        values = {'first_name': user.first_name,
                  'last_name': user.last_name}
        editProfileForm = EditUserForm(instance = userprofile, initial = values)
        return render_to_response('users/edit_profile.html', locals(),context_instance=RequestContext(request))
        
@login_required
def SiteCSVRegn(request):
    if not request.user.get_profile().is_hospi:
        return HttpResponseRedirect(settings.SITE_URL)
    msg = ''
    form = SiteCSVRegnForm()
    if request.method == 'POST':
        form = SiteCSVRegnForm(request.POST, request.FILES)   
        if form.is_valid():
            alreadyCreated = []
            noEmail = []
            freshCreations = []
            badBarcode = []
            numLines = 0
            numCreations = 0
            for line in form.cleaned_data['new_registrations_file']:
                numLines += 1
                line = line.replace('\n', '').replace('\r', '')
                if line == '':
                    continue
                recordDetails = line.split(',')
                (BARCODE, USERNAME, FIRSTNAME, LASTNAME, EMAIL, MOBILE, GENDER, AGE, COLLEGE) = range(9)
                if len(recordDetails[BARCODE]) != 5:
                    badBarcode.append(line)
                    continue
                try:
                    user = User.objects.get(username = recordDetails[USERNAME],email = recordDetails[EMAIL])
                    profile = UserProfile.objects.get(user = user)
                    if user and profile:
                        newParticipant = Participant.objects.get(shaastra_id = profile.shaastra_id)
                        try:
                            Barcodemap.objects.get(shaastra_id = newParticipant)
                        except:
                            newBarcode = BarcodeMap()
                            newBarcode.shaastra_id = newParticipant
                            newBarcode.barcode = recordDetails[BARCODE]
                            newBarcode.save(using = 'erp')
                except User.DoesNotExist:
                    # Create new user
                    newUser = User()
                    try:
                        usr = User.objects.get(username = recordDetails[USERNAME])
                    except:
                        pass
                    if not recordDetails[EMAIL]:
                        noEmail.append(line)
                        continue
                    newUser.email = recordDetails[EMAIL]
                    if recordDetails[USERNAME]:
                        if usr:
                            newUser.username = recordDetails[EMAIL]+'__123'
                        else:
                            newUser.username = recordDetails[USERNAME]    
                    else:
                        newUser.username = recordDetails[EMAIL].split('@')[0]
                    if recordDetails[FIRSTNAME]:
                        newUser.first_name = recordDetails[FIRSTNAME]
                    else:
                        newUser.first_name = recordDetails[EMAIL].split('@')[0]
                    if recordDetails[LASTNAME]:
                        newUser.last_name = recordDetails[LASTNAME]
                    newUser.set_password('default')
                    newUser.is_active = True
                    newUser.save()
                    newUserProfile = UserProfile(user=newUser)
                    # Get the college
                    try:
                        try:
                            newCollege = College.objects.get(name = recordDetails[COLLEGE])
                        except:
                            newCollege = College.objects.filter(name = recordDetails[COLLEGE])[0] 
                        else:
                            pass
                    except College.DoesNotExist:
                        # Create the college
                        if not newCollege:
                            newCollege = College()
                            newCollege.name = recordDetails[COLLEGE]
                            newCollege.city = 'Unknown'
                            newCollege.save()
                        newUserProfile.gender = 'F'
                    if recordDetails[AGE]:
                        newUserProfile.age = recordDetails[AGE]
                    else:
                        newUserProfile.age = 0
                    newUserProfile.shaastra_id = 'SHA' + str(1300000 + newUser.id)
                    newUserProfile.college = newCollege
                    newUserProfile.college_roll = 'CollegeRoll'
                    newUserProfile.branch = 'Others'
                    newUserProfile.want_accomodation = False
                    newUserProfile.save()
                    
                    #New participant
                    newParticipant = Participant()
                    newParticipant.name = newUser.first_name + ' ' + newUser.last_name
                    newParticipant.gender = newUserProfile.gender
                    newParticipant.age = newUserProfile.age
                    newParticipant.branch = newUserProfile.branch
                    newParticipant.mobile_number = newUserProfile.mobile_number
                    newParticipant.shaastra_id = newUserProfile.shaastra_id
                    newParticipant.save(using = 'erp')

                    # Map to barcode
                    newBarcode = BarcodeMap()
                    newBarcode.shaastra_id = newParticipant
                    newBarcode.barcode = recordDetails[BARCODE]
                    newBarcode.save(using = 'erp')

                    freshCreations.append((newUser.username, newUserProfile.shaastra_id, recordDetails[BARCODE]))
                    numCreations += 1
                else:
                    # Already exists
                    alreadyCreated.append(line)
            finalstats = ''
            finalstats += 'Number of accounts created: %d<br/>' % numCreations
            if numCreations > 0:
                finalstats += '<br/>The following accounts were created:'
                finalstats += '<table class="table table-striped table-bordered table-condensed"><tr><th>Username</th><th>Shaastra ID</th><th>Barcode</th></tr>'
                for creationRecord in freshCreations:
                    finalstats += '<tr><td>'+creationRecord[0]+'</td><td>'+creationRecord[1]+'</td><td>'+creationRecord[2]+'</td></tr>'
                finalstats += '</table>'
            if alreadyCreated:
                finalstats += '<br/>The following records were not created (existing email used).<br/>'
                for line in alreadyCreated:
                    finalstats += line + '<br/>'
            if noEmail:
                finalstats += '<br/>The following records were not created (no email present).<br/>'
                for line in noEmail:
                    finalstats += line + '<br/>'
            if badBarcode:
                finalstats += '<br/>The following records were not created (bad barcode - should be 5 digits).<br/>'
                for line in badBarcode:
                    finalstats += line + '<br/>'
                
            msg = finalstats
            
    return render_to_response('controlroom/SiteCSVRegn.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def editallot(request):
    if not request.user.get_profile().is_hospi:
        return HttpResponseRedirect(settings.SITE_URL)
    if request.method=='POST':
        form = request.POST
        #try:
        checkedin = IndividualCheckIn.objects.get(shaastra_ID = form['shaastra_ID'])
        rm = checkedin.room
        individual_form=IndividualForm(form,croom=checkedin.room,instance=checkedin)
        if individual_form.is_valid():
            rm.already_checkedin = rm.already_checkedin - 1
            rm.mattresses = rm.mattresses - checkedin.number_of_mattresses_given 
            rm.save()
            form1 = individual_form.save(commit=False)
            form1.check_out_date = None
            room = AvailableRooms.objects.get(id = form1.room_id)
            room.already_checkedin = room.already_checkedin + 1
            room.mattresses = room.mattresses + form1.number_of_mattresses_given 
            room.save()
            #assert False
            form1.save()
            msg = "Updated Successfully!"
        else:
            msg = "Invalid Form1"
        '''
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
        '''
    else:
        msg = "GOBACK"
    return render_to_response('controlroom/individual.html', locals(),context_instance=RequestContext(request))
