#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import cgi
import json

from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from users.forms import AddUserForm, FacebookUserForm
from users.models import UserProfile
from django.conf import settings


def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {'client_id': settings.FACEBOOK_APP_ID,
            'scope': settings.FACEBOOK_SCOPE,
            'redirect_uri': request.build_absolute_uri(settings.SITE_URL
            + 'user/facebook/authentication_callback/')}

    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?'
                                 + urllib.urlencode(args))


def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """

    code = request.GET.get('code')

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': request.build_absolute_uri(settings.SITE_URL
                + 'user/facebook/authentication_callback/'),
        'code': code,
        }

    # Get a legit access token

    target = \
        urllib.urlopen('https://graph.facebook.com/oauth/access_token?'
                       + urllib.urlencode(args)).read()
    response = cgi.parse_qs(target)
    access_token = response['access_token'][-1]

#    access_token = authenticate(token=code, request=request)

    # Read the user's profile information

    fb_profile = \
        urllib.urlopen('https://graph.facebook.com/me?access_token=%s'
                       % access_token)
    fb_profile = json.load(fb_profile)

    try:

        # Try and find existing user

        fb_user = \
            UserProfile.objects.get(facebook_id=str(fb_profile['id']))
        user = authenticate(username=fb_user.user, password='default')
        if user is not None:
            auth_login(request, user)
        return HttpResponseRedirect(settings.SITE_URL)
    except UserProfile.DoesNotExist:

        # No existing user
        # Not all users have usernames

        username = fb_profile.get('username', fb_profile['email'
                                  ].split('@')[0])
        email = fb_profile['email']
        first_name = fb_profile['first_name']
        last_name = fb_profile['last_name']
        facebook_id = str(fb_profile['id'])
        password = 'default'
        password_again = 'default'
        if fb_profile['gender'] == 'female':
            gender = 'F'
        else:
            gender = 'M'
        post_url = settings.SITE_URL + 'user/register_fb/'
        form = FacebookUserForm(initial=locals())
    return render_to_response('users/register.html', locals(),
                              context_instance=RequestContext(request))


