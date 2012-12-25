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
from events.models import Event
from users.models import UserProfile, College
from django.utils.translation import ugettext as _
from users.forms import *
from django.contrib.sessions.models import Session
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.mail import send_mail as mailsender
from recaptcha.client import captcha
import sha
import random
import datetime


def login_get(request):
    if request.user.is_authenticated():
        currentuser = request.user
        if request.user.is_superuser:
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif currentuser.get_profile().is_core:
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif currentuser.get_profile().is_coord_of:
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
        elif currentuser.get_profile().is_hospi:
            return HttpResponseRedirect(settings.SITE_URL + 'controlroom/home/')
        else:
            return HttpResponseRedirect(settings.SITE_URL)
    form = LoginForm()
    try:
        msg=request.session['msg']
        del request.session['msg']
    except:
        pass
    return render_to_response('users/login.html', locals(),
                              context_instance=RequestContext(request))


def login_post(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth_login(request, user)
        try:
            nextURL = request.GET['next']
        except:
            nextURL = ''
        if nextURL != '':
            nextURL = nextURL[1:]  # For removing the leading slash from in front of the next parameter
            redirectURL = settings.BASE_URL + nextURL
            return HttpResponseRedirect(redirectURL)
        if user.is_superuser:
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif user.get_profile().is_core:
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif user.get_profile().is_coord_of:
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
        elif user.get_profile().is_hospi:
            return HttpResponseRedirect(settings.SITE_URL + 'controlroom/home/')
        else:
            return HttpResponseRedirect(settings.SITE_URL)
    msg = 'Username and Password does not match.'
    form = LoginForm()
    return render_to_response('users/login.html', locals(),
                              context_instance=RequestContext(request))


#@login_required(login_url=settings.SITE_URL + 'user/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(settings.SITE_URL)


def register_get(request):
    form = AddUserForm()
    post_url = settings.SITE_URL + 'user/register/'
    captcha_response = ''  # Added so that nothing gets displayed in the template if this variable is not set
    return render_to_response('users/register.html', locals(),
                              context_instance=RequestContext(request))


def register_post(request):
    """
        This is the user registration view
    """

    form = AddUserForm(request.POST)
    captcha_response = ''  # Added so that nothing gets displayed in the template if this variable is not set
    
    # talk to the reCAPTCHA service
    response = captcha.submit(  
        request.POST.get('recaptcha_challenge_field'),  
        request.POST.get('recaptcha_response_field'),  
        settings.RECAPTCHA_PRIVATE_KEY,  
        request.META['REMOTE_ADDR'],)  
          
    # see if the user correctly entered CAPTCHA information  
    # and handle it accordingly.  
    if response.is_valid:  
        if form.is_valid():
            data = form.cleaned_data
            new_user = User(first_name=data['first_name'],
                            last_name=data['last_name'],
                            username=data['username'], email=data['email'])
            new_user.set_password(data['password'])
            new_user.is_active = False
            new_user.save()
            x = 1300000 + new_user.id 
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            userprofile = UserProfile(
                user=new_user,
                activation_key=activation_key,
                key_expires=key_expires,
                gender=data['gender'],
                age=data['age'],
                branch=data['branch'],
                mobile_number=data['mobile_number'],
                college=data['college'],
                college_roll=data['college_roll'],
                shaastra_id= ("SHA" + str(x)),
                want_accomodation = data['want_accomodation'],
                )
            userprofile.save()
            mail_template = get_template('email/activate.html')
            body = \
                mail_template.render(Context({'username': new_user.username,
                                     'SITE_URL': settings.SITE_URL,
                                     'activationkey': userprofile.activation_key}))
            mailsender('Your new Shaastra2013 account confirmation', body,
                       'noreply@shaastra.org', [new_user.email],
                       fail_silently=False)
            request.session['registered_user'] = True
            request.session['msg']="A mail has been sent to the mail id you provided. Please activate your account within 48 hours. Check your spam folder if you do not receive the mail in your inbox."
            return HttpResponseRedirect(settings.SITE_URL+'user/login')
    else:
        captcha_response = response.error_code
    return render_to_response('users/register.html', locals(),
                              context_instance=RequestContext(request))


def register_post_fb(request):
    """
        This is the user registration view for fb
    """

    form = FacebookUserForm(request.POST)
    facebook_id = request.POST['facebook_id']
    access_token = request.POST['access_token']
    if form.is_valid():
        data = form.cleaned_data
        new_user = User(first_name=data['first_name'],
                        last_name=data['last_name'],
                        username=data['username'], email=data['email'])
        new_user.set_password('default')
        new_user.save()
        x = 1300000 + new_user.id 
        userprofile = UserProfile(
            user=new_user,
            gender=data['gender'],
            age=data['age'],
            branch=data['branch'],
            mobile_number=data['mobile_number'],
            college=data['college'],
            college_roll=data['college_roll'],
            facebook_id=facebook_id,
            access_token=access_token,
            shaastra_id = "SHA" + str(x),
            )
        userprofile.save()
        new_user = authenticate(username=data['username'],
                                password='default')
        auth_login(request, new_user)
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('users/register.html', locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/login/')
def editprofile_get(request):
    currentUser = request.user
    currentUserProfile = currentUser.get_profile()
    values = {'first_name': currentUser.first_name,
              'last_name': currentUser.last_name}
    editProfileForm = EditUserForm(instance=currentUserProfile,
                                   initial=values)
    if request.user.get_profile().is_core \
        or request.user.get_profile().is_coord_of:
        return render_to_response('users/edit_profile_c.html',
                                  locals(),
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('users/edit_profile.html', locals(),
                                  context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/login/')
def editprofile_post(request):
    """
        Edits a user's profile. 
        
    """

    currentUser = request.user
    currentUserProfile = currentUser.get_profile()
    editProfileForm = EditUserForm(request.POST,
                                   instance=currentUserProfile)
    if editProfileForm.is_valid():
        editProfileForm.save()
        currentUser.first_name = request.POST['first_name']
        currentUser.last_name = request.POST['last_name']
        currentUser.save()
        return HttpResponseRedirect(settings.SITE_URL)
    if request.user.get_profile().is_core \
        or request.user.get_profile().is_coord_of:
        return render_to_response('users/edit_profile_c.html',
                                  locals(),
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('users/edit_profile.html', locals(),
                                  context_instance=RequestContext(request))


def activate(request, a_key=None):
    """
       The activation_key (a_key) is trapped from the url. If the key is not empty then the corresponding userprofile object is retrieved. If the object doesn't exist and ObjectDoesNotExist error is flagged.
       
       The the key has already expired then the userprofile and the corresponding user objects are deleted, otherwise, the is_active field in the user model is set to true.
       
       Note that, if is_active is not set to true, the user cannot login. 
    """

    SITE_URL = settings.SITE_URL
    if a_key == '' or a_key == None:
        key_dne = True
    else:
        try:
            user_profile = UserProfile.objects.get(activation_key=a_key)
        except ObjectDoesNotExist:
            prof_dne = True
        else:

        # try-except-else is actually there! God knows what for... Nested try blocks work just as well...

            if user_profile.user.is_active == True:
                activated = True
            elif user_profile.key_expires < datetime.datetime.today():
                expired = True
                user = user_profile.user
                user.delete()
                user_profile.delete()
            else:
                user = user_profile.user
                user.is_active = True
                x = 1300000 + user.id 
                user_profile.shaastra_id = "SHA"+ str(x)
                user_profile.save()
                user.save()
                request.session['registered'] = True
                activated = True
    return render_to_response('users/activated.html', locals(),
                              context_instance=RequestContext(request))


def events(request):
    event = Event.objects.all()
    return render_to_response('users/events.html', locals(),
                              context_instance=RequestContext(request))


def ajax_login_link(request):
    return HttpResponse('<a href="%suser/login">Click here to login</a>'
                         % settings.SITE_URL)
                         
### Views for teams:

def get_authentic_team(request = None, team_id = None):
    if team_id is None or request is None:
        return None
    try:
        team = Team.objects.get(pk = int(team_id))
        try:
            team.members.get(pk = request.user.id)
            return team
        # Non-members fail the test
        except User.DoesNotExist:
            return None
    except Team.DoesNotExist:
        return None
    return None

@login_required
def team_home(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        add_member_form = AddMemberForm()
        change_leader_form = ChangeLeaderForm()
        event = team.event
        team_size = team.members.count()
        if team_size > event.team_size_max:
            team_size_message = 'big'
        elif team_size < event.team_size_min:
            team_size_message = 'small'
        else:
            team_size_message = 'correct'
        return render_to_response('users/teams/team_home.html', locals(), context_instance = RequestContext(request))
    raise Http404

@login_required
def create_team(request, event_id = None):
    if event_id is None:
        raise Http404
    user = request.user
    try:
        event = Event.objects.get(pk = int(event_id))
    except:
        raise Http404('You have requested for an invalid event.')
    if not event.begin_registration:
        raise Http404('The registrations for this event have closed. New teams can no longer be registered.')
    form = CreateTeamForm(initial = {'event' : event.id, } )
    view = "Create"
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            try:
                Team.objects.get(members__pk = request.user.id, event = form.cleaned_data['event'])
                return render_to_response('users/teams/already_part_of_a_team.html', locals(), context_instance = RequestContext(request))
            except Team.DoesNotExist:
                pass
            team = form.save(commit = False)
            team.leader = user
            '''
            try:
                team.leader.get_profile().registered.get(pk = team.event.id)
            except Event.DoesNotExist:
                team.leader.get_profile().registered.add(team.event)
            '''
            team.save()
            team.members.add(user)
            return HttpResponseRedirect('%suser/teams/%s/' % (settings.SITE_URL, team.id))
    return render_to_response('users/teams/create_team.html', locals(), context_instance = RequestContext(request))

'''
def join_team(request):
    user = request.user
    form = JoinTeamForm()
    view = "Join"
    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(name = form.cleaned_data['name'], event = form.cleaned_data['event'])
            team.join_requests.add(user)
            return HttpResponseRedirect('%smyshaastra/' % settings.SITE_URL)
    return render_to_response('myshaastra/team_form.html', locals(), context_instance = RequestContext['request'])
'''

@login_required
def add_member(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        event = team.event
        team_size = team.members.count()
        if team_size == event.team_size_max:
            raise Http404('Your team is already of the maximum permitted size. You cannot add more people to the team without removing someone.')
        add_member_form = AddMemberForm()
        change_leader_form = ChangeLeaderForm()

        if team_size > event.team_size_max:
            team_size_message = 'big'
        elif team_size < event.team_size_min:
            team_size_message = 'small'
        else:
            team_size_message = 'correct'

        if request.method == 'POST':
            user = request.user
            add_member_form = AddMemberForm(request.POST)
            if add_member_form.is_valid():
                if user != team.leader:
                    return render_to_response('users/teams/you_arent_leader.html', locals(), context_instance = RequestContext(request))
                member = User.objects.get(username = add_member_form.cleaned_data['member'])
                '''
                # autoregister member on addition to the team
                try:
                    member.get_profile().registered.get(pk = team.event.id)
                except Event.DoesNotExist:
                    member.get_profile().registered.add(team.event)
                '''
                team.members.add(member)
                return HttpResponseRedirect('%suser/teams/%s/' % (settings.SITE_URL, team.id))
            else:
                try:
                    if add_member_form['member'].errors != []:
                        return render_to_response(
                            'users/teams/already_part_of_a_team.html', 
                            { 'user' : request.POST['member'], }, 
                            context_instance = RequestContext(request)
                        )
                except KeyError:
                    pass
        return render_to_response('users/teams/team_home.html', locals(), context_instance = RequestContext(request))
    raise Http404

@login_required
def change_team_leader(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        change_leader_form = ChangeLeaderForm()
        add_member_form = AddMemberForm()
        if request.method == 'POST':
            user = request.user
            change_leader_form = ChangeLeaderForm(request.POST)
            if change_leader_form.is_valid():
                if user != team.leader:
                    return render_to_response('users/teams/you_arent_leader.html', locals(), context_instance = RequestContext(request))
                new_leader = team.members.get(username = change_leader_form.cleaned_data['new_leader'])
                team.leader = new_leader
                team.save()
                return HttpResponseRedirect('%suser/teams/%s/' % (settings.SITE_URL, team.id))
        return render_to_response('users/teams/team_home.html', locals(), context_instance = RequestContext(request))
    raise Http404

@login_required
def drop_out(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        user = request.user
        if user == team.leader:
            return render_to_response('users/teams/you_are_leader.html', locals(), context_instance = RequestContext(request))
        else:
            team.members.remove(user)
            return HttpResponseRedirect('%sevents/' % settings.SITE_URL)
    raise Http404

@login_required
def remove_member(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        change_leader_form = ChangeLeaderForm()            # it is the same form essentially :P
        add_member_form = AddMemberForm()
        if request.method == 'POST':
            user = request.user
            change_leader_form = ChangeLeaderForm(request.POST)
            if change_leader_form.is_valid():
                team = Team.objects.get(pk = change_leader_form.cleaned_data['team_id'])
                if user != team.leader:
                    return render_to_response('users/teams/you_arent_leader.html', locals(), context_instance = RequestContext(request))
                new_leader = team.members.get(username = change_leader_form.cleaned_data['new_leader'])           
                team.members.remove(new_leader)                                                # yes i know, it looks bad. but what the hell. i'm lazy.
                return HttpResponseRedirect('%suser/teams/%s/' % (settings.SITE_URL, team.id))
        return render_to_response('users/teams/team_home.html', locals(), context_instance = RequestContext(request))
    raise Http404

@login_required
def dissolve_team(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        if team.members.all().count() > 1:
            return render_to_response('users/teams/remove_members_first.html', locals(), context_instance = RequestContext(request))
        else:
            if team.leader != request.user:
                return render_to_response('users/teams/you_arent_leader.html', locals(), context_instance = RequestContext(request))
            team.members.clear()
            team.delete()
            return HttpResponseRedirect('%sevents/' % settings.SITE_URL)
    raise Http404

