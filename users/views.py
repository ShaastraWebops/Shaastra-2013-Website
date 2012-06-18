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
        if request.user.is_superuser :
            return HttpResponseRedirect('/user/admin')
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
            return HttpResponseRedirect('/user/admin')
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

@login_required(login_url='/user/login')
def admin(request):
    """
        This is the home page view of the superuser
    """

    if request.user.is_superuser :
        return render_to_response('users/admin.html', locals(), context_instance = RequestContext(request))
    else:
        return HttpResponseRedirect('/')

@login_required
def edit_profile(request):
    """
    create_or_edit_profile():
        Edits a user's profile. 
        If a user does not have a profile, creates a blank profile for that user and then allows editing.
    """
    currentUser = request.user
    try:
        currentUserProfile = currentUser.get_profile()
    except:
        currentUserProfile = UserProfile()
        currentUserProfile.user = currentUser
        currentUserProfile.save()
    if request.method == 'POST':
        editProfileForm = forms.EditUserForm(request.POST)
        if editProfileForm.is_valid():
            newProfileInfo = editProfileForm.cleaned_data
            currentUser.first_name = newProfileInfo['first_name']
            currentUser.last_name = newProfileInfo['last_name']
            currentUserProfile.gender = newProfileInfo['gender']
            currentUserProfile.age = newProfileInfo['age']
            currentUserProfile.branch = newProfileInfo['branch']
            currentUserProfile.mobile_number = newProfileInfo['mobile_number']
            currentUserProfile.college = newProfileInfo['college']
            currentUserProfile.college_roll = newProfileInfo['college_roll']
            currentUserProfile.want_hospi = newProfileInfo['want_hospi']
            currentUser.save()
            currentUserProfile.save()
            redirect_to="/"
            return HttpResponseRedirect (redirect_to)
    else:
        values = {'first_name' : currentUser.first_name, 
                  'last_name' : currentUser.last_name,
                  'gender' : currentUserProfile.gender,
                  'age' : currentUserProfile.age,
                  'branch' : currentUserProfile.branch,
                  'mobile_number' : currentUserProfile.mobile_number, 
                  'college' : currentUserProfile.college,                 
                  'college_roll' : currentUserProfile.college_roll,
                  'want_hospi' : currentUserProfile.want_hospi}
        editProfileForm = forms.EditUserForm(initial = values)

    return render_to_response('edit_profile.html', locals(), context_instance = RequestContext(request))
