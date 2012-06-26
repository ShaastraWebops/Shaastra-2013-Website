from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User, Group
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from users.models import UserProfile, College
from users.forms import *

def login_get(request):
    if request.user.is_authenticated() :
        currentuser=request.user
        currentUserProfile=currentuser.get_profile()
        if request.user.is_superuser :
            return HttpResponseRedirect('/admin')
        elif currentUserProfile.is_core :
            return HttpResponseRedirect('/core')
        else:
            return HttpResponseRedirect('/')
    form = LoginForm()
    return render_to_response('users/login.html',locals(),context_instance = RequestContext(request))
    
def login_post(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth_login(request, user)
        if user.is_superuser :
            return HttpResponseRedirect('/admin')
        elif user.get_profile().is_core :
            return HttpResponseRedirect('/core')
    return HttpResponseRedirect('/')

@login_required(login_url='/user/login')    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def register_get(request):
    form = AddUserForm()
    return render_to_response('users/register.html', locals(), context_instance = RequestContext(request))    
    
def register_post(request):
    """
        This is the user registration view
    """
    form = AddUserForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        new_user = User(first_name = data['first_name'], last_name=data['last_name'], username= data['username'], email = data['email'])
        new_user.set_password(data['password'])
        new_user.save()
        userprofile = UserProfile(
                user = new_user,
                gender     = data['gender'],
                age = data['age'],
                branch = data['branch'],
                mobile_number = data['mobile_number'],
                college = data['college'],
                college_roll = data['college_roll'],
                )
        userprofile.save()
        new_user = authenticate(username = data['username'], password = data['password'])
        auth_login(request, new_user)
        return HttpResponseRedirect('/')
    return render_to_response('users/register.html', locals(), context_instance = RequestContext(request))


@login_required(login_url="/user/login")
def editprofile_get(request):
    currentUser = request.user
    currentUserProfile = currentUser.get_profile()
    values = {  'first_name'       : currentUser.first_name, 
                'last_name'      : currentUser.last_name,}
    editProfileForm = EditUserForm(instance=currentUserProfile,initial=values)
    return render_to_response('users/edit_profile.html', locals(), context_instance = RequestContext(request))    

@login_required(login_url="/user/login")
def editprofile_post(request):
    """
        Edits a user's profile. 
        
    """
    currentUser = request.user
    currentUserProfile = currentUser.get_profile()
    editProfileForm = EditUserForm(request.POST,instance=currentUserProfile)
    if editProfileForm.is_valid():
        editProfileForm.save()
        currentUser.first_name = request.POST['first_name']
        currentUser.last_name = request.POST['last_name']
        currentUser.save()
        return HttpResponseRedirect ("/")
    return render_to_response('users/edit_profile.html', locals(), context_instance = RequestContext(request))
