import urllib, cgi,json

from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from users.forms import AddUserForm, UserRegisterForm
from users.models import UserProfile


def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))

def authentication_callback(request):
    """ Second step of the login process.
    It reads in a code from Facebook, then redirects back to the home page. """
    code = request.GET.get('code')

    """ Reads in a Facebook code and asks Facebook if it's valid and what user it points to. """
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
        'code': code,
    }

    # Get a legit access token
    target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
    response = cgi.parse_qs(target)
    access_token = response['access_token'][-1]

#    access_token = authenticate(token=code, request=request)

    # Try and find existing user
    fb_user=UserProfile.objects.get(user=request.user)
    fb_user.access_token=access_token
    fb_user.save()
    return HttpResponseRedirect("/osqa")
