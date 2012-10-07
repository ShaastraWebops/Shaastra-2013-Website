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
        nextURL = request.GET.get('next', '')
        if nextURL != '':
            nextURL = nextURL[1:]  # For removing the leading slash from in front of the next parameter
            redirectURL = settings.SITE_URL + nextURL
            return HttpResponseRedirect(redirectURL)
        if user.is_superuser:
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif user.get_profile().is_core:
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif user.get_profile().is_coord_of:
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
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
                x = (100000 + user.id) % 10000
                user_profile.shaastra_id = "SHA13"+ x
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
