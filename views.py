from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib import *
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from forms import*
from django.contrib.auth import authenticate, login, logout

def home(request):
	return render_to_response('home.html',locals(),context_instance = RequestContext(request))
	
def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404

def login_get(request):
    errors = False
    return render_to_response('login.html',locals(),context_instance = RequestContext(request))
    
def login_post(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    errors = True
    return render_to_response('login.html',locals(),context_instance = RequestContext(request))
    
def log_out(request):
    logout(request)
    return HttpResponse('You have been Logged Out successfully.<a href="/">Home</a>')

def register_get(request):
    form = RegistrationForm()
    return render_to_response('register.html', locals(), context_instance = RequestContext(request))    
    
def register_post(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        new_user = User(first_name = data['first_name'], username = data['username'], email = data['email'])
        new_user.set_password(data['password'])
        new_user.save()
        new_user = authenticate(username = data['username'], password = data['password'])
        login(request, new_user)
        return HttpResponseRedirect('/')
    return render_to_response('register.html', locals(), context_instance = RequestContext(request))
    
