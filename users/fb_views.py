import urllib, cgi,json

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import login as auth_login, authenticate
from django.core.urlresolvers import reverse
from django.conf import settings
from users.forms import BaseUserForm
from users.models import UserProfile

def login(request):
    """ First step of process, redirects user to facebook, which redirects to authentication_callback. """

    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': 'http://127.0.0.1:8000/user/facebook/authentication_callback',
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
        'redirect_uri': 'http://127.0.0.1:8000/user/facebook/authentication_callback',
        'code': code,
    }

    # Get a legit access token
    a='https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)
    target = urllib.urlopen(a).read()
    response = cgi.parse_qs(target)
    access_token = response['access_token'][-1]

#    access_token = authenticate(token=code, request=request)

    # Read the user's profile information
    fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
    fb_profile = json.load(fb_profile)

    try:
        # Try and find existing user
        fb_user = UserProfile.objects.get(facebook_id=fb_profile['id'])
        user=authenticate(username=fb_user.user.email,password="default")
        if user is not None:
            auth_login(request,user)
        return HttpResponseRedirect('/')
    except UserProfile.DoesNotExist:
        # No existing user
        # Not all users have usernames
#        username = fb_profile.get('username', fb_profile['email'].split('@')[0])
        email=fb_profile['email']
        first_name = fb_profile['first_name']
        last_name = fb_profile['last_name']
        facebook_id=fb_profile['id']
        password="default"
        password_again="default"
        if fb_profile['gender'] == "female" :
            gender='F'
        else:
            gender='M'
        form = BaseUserForm(initial=locals())
    return render_to_response('users/register.html',locals(), context_instance=RequestContext(request))    

