import cgi, urllib, json

from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db import IntegrityError

from users.models import UserProfile 

class FacebookBackend:
    def authenticate(self, token=None, request=None):
        """ Reads in a Facebook code and asks Facebook if it's valid and what user it points to. """
        args = {
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'redirect_uri': request.build_absolute_uri('/facebook/authentication_callback'),
            'code': token,
        }

        # Get a legit access token
        target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
        response = cgi.parse_qs(target)
        access_token = response['access_token'][-1]

        # Read the user's profile information
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % access_token)
        fb_profile = json.load(fb_profile)

        try:
            # Try and find existing user
            fb_user = UserProfile.objects.get(facebook_id=fb_profile['id'])
            user = fb_user.user

            # Update access_token
            fb_user.access_token = access_token
            fb_user.save()
            
            settings.LOGIN_REDIRECT_URL="/login"

        except UserProfile.DoesNotExist:
            # No existing user

            # Not all users have usernames
            username = fb_profile.get('username', fb_profile['email'].split('@')[0])
            
            settings.LOGIN_REDIRECT_URL="/register/user"            
            '''
            if getattr(settings, 'FACEBOOK_FORCE_SIGNUP', False):
                # No existing user, use anonymous
                user = AnonymousUser()
                user.username = username
                user.first_name = fb_profile['first_name']
                user.last_name = fb_profile['last_name']
                fb_user = UserProfile(
                        facebook_id=fb_profile['id'],
                        access_token=access_token
                )
                user.facebookprofile = fb_user

            else:
            '''
            # No existing user, create one

            try:
                user = User.objects.create_user(username, fb_profile['email'])
            except IntegrityError:
                # Username already exists, make it unique
                user = User.objects.create_user(username + fb_profile['id'], fb_profile['email'])
            user.first_name = fb_profile['first_name']
            user.last_name = fb_profile['last_name']
            user.save()
            # Create the FacebookProfile
            fb_user = UserProfile(user=user, facebook_id=fb_profile['id'], access_token=access_token)
            if fb_profile['gender'] == "female" :
                fb_user.gender='F'
            else:
                fb_user.gender='M'
            fb_user.save()

        return user

    def get_user(self, user_id):
        """ Just returns the user of a given ID. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    supports_object_permissions = False
    supports_anonymous_user = True
