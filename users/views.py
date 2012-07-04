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
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif currentUserProfile.is_core :
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif currentUserProfile.is_coord_of :
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
        else:
            return HttpResponseRedirect(settings.SITE_URL)
    form = LoginForm()
    return render_to_response('users/login.html',locals(),context_instance = RequestContext(request))
    
def login_post(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth_login(request, user)
        if user.is_superuser :
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif user.get_profile().is_core :
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif user.get_profile().is_coord_of :
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
    return HttpResponseRedirect(settings.SITE_URL)

@login_required(login_url=settings.SITE_URL + 'user/login/')    
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(settings.SITE_URL)

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
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('users/register.html', locals(), context_instance = RequestContext(request))


@login_required(login_url=settings.SITE_URL + "user/login/")
def editprofile_get(request):
    currentUser = request.user
    currentUserProfile = currentUser.get_profile()
    values = {  'first_name'       : currentUser.first_name, 
                'last_name'      : currentUser.last_name,}
    editProfileForm = EditUserForm(instance=currentUserProfile,initial=values)
    return render_to_response('users/edit_profile.html', locals(), context_instance = RequestContext(request))    

@login_required(login_url=settings.SITE_URL + "user/login/")
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
        return HttpResponseRedirect (settings.SITE_URL)
    return render_to_response('users/edit_profile.html', locals(), context_instance = RequestContext(request))
'''
def forgot_password(request):
    reset_password_form = forms.ResetPasswordForm()
    username_form = forms.UsernameForm()
    if request.method == 'GET' and 'password_key' in request.GET:
        try:
            profile = UserProfile.objects.get(activation_key = request.GET['password_key'])
            profile.save()
            user = profile.user
            reset_password_form = forms.ResetPasswordForm(initial = {'user' : user.id, })
            return render_to_response('users/reset_password_form.html', locals(), context_instance = global_context(request))
        except UserProfile.DoesNotExist:
            raise Http404
    elif request.method == 'POST':
        username_form = forms.UsernameForm(request.POST)
        if username_form.is_valid():
            username = username_form.cleaned_data['username']
            user = User.objects.get(username = username)
            profile = user.get_profile()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            profile.activation_key = sha.new(salt+user.username).hexdigest()
            profile.save()
            
            mail_template = get_template('email/forgot_password.html')
            body = mail_template.render(Context( {
                'username' : user.username,
                'SITE_URL' : settings.SITE_URL,
                'passwordkey' : profile.activation_key 
            } ))
            send_mail('[Shaastra 2011] Password reset request', body,'noreply@shaastra.org', [user.email,], fail_silently = False)
            return HttpResponseRedirect('%smyshaastra/forgot_password/done/' % settings.SITE_URL)
    return render_to_response('users/username_form.html', locals(), context_instance = global_context(request))
'''
