from django.http import HttpResponse, HttpResponseRedirect, Http404
#from django.core.exceptions import ObjectDoesNotExist
#from django.contrib import auth
from django.contrib.auth.models import User, Group
#from django.template.loader import get_template
from django.template.context import Context, RequestContext
#from django.utils.translation import ugettext as _
#from django.core.mail import send_mail,EmailMessage,SMTPConnection
#from django.contrib.sessions.models import Session
#from django.utils import simplejson

#from  misc.util import *
from  users.models import UserProfile
#from  users import models
from  users import forms

#import sha,random,datetime
#from django.core.mail import EmailMultiAlternatives

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as log_in, logout as log_out

def login (request):
    """
        This is the view for logging a user in.
        If the user is already logged in and is a core or coord, he is redirected to the dashboard.
        Normal users are redirected to the home page.
        
        If the user who logs in is a core or coord, he is redirected to the dashboard. 
        If normal users login, he/she is redirected to the previous url. If this fails, he/she is 
        redirected to the home page.
    """    
    form=forms.LoginForm()
    if(request.method=='POST'):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            inputs = form.cleaned_data
            user = authenticate(username=inputs['username'],password=inputs['password'])
            if user is not None:
                log_in(request, user)
                return HttpResponseRedirect("/login")
            else:                
                return HttpResponse("Invalid")

    try:
        facebook_profile = request.user.get_profile().get_facebook_profile()
    except:
        try:
            twitter_profile = request.user.get_profile().get_twitter_profile()
        except:
            form = forms.LoginForm()
            return render_to_response('login.html',locals(), context_instance=RequestContext(request))
        return render_to_response('login.html',locals(), context_instance=RequestContext(request))
    return render_to_response('login.html',locals(), context_instance=RequestContext(request))


'''
@needs_authentication
def spons_dashboard(request):
    if request.user.username == 'spons':
        return render_to_response('users/spons_dashboard.html', locals(), context_instance = global_context(request))
    raise Http404
'''

def logout(request):
    """
        If username is cores or spons, the coord_event is set to none and the userprofile is saved.
        The user is then logged out using the default django view.
              
        In case the user is not logged in and tries to visit the logout url, he/she is redirected to the login page.
        Nice touch. :)
    
    
    if request.user.is_authenticated():
        if request.user.username == 'cores' or request.user.username == 'spons':
            userprofile = request.user.get_profile()
            userprofile.coord_event = None
            userprofile.save()
        auth.logout (request)
        request.session['logged_in'] = False
        return render_to_response('users/logout.html', locals(), context_instance= global_context(request))        
    return HttpResponseRedirect('%slogin/'%settings.SITE_URL) 
    """
    log_out(request)
    return HttpResponseRedirect('/login')       

    
def user_registration(request):
    """ 
        If the user is already logged it, set logged_in to true. He/she won't be allowed to register.
        
        Retrieve the list of colleges and display them as coll.name,coll.city . This list is used for the jquery autocompletion. 
        js_data is a simplejson dump of the list of collnames. 
        
        ...var data = {{js_data|safe}};
        ...$("#coll_input").autocomplete(data);
        
        These two lines in the template handle the autocomplete for college selection. ( The id of the college field is set to coll_input in forms.py. You need to include the jquery autocomplete plugin for it to work.
        
        If the request method is post and the form is valid , a user object is created and the is_active attribute is set to false.
        
        A random activation_key is generated and the expiry is set to 2 days fromt the point of registration.
        
        The userprofile object is created with the foreign key set the user object previously created.
        
    """ 
#    colls = models.College.objects.all()
#    collnames = list()
#    for coll in colls:
#        collnames.append(coll.name + "," + coll.city)
#    js_data = simplejson.dumps(collnames)

    if request.method=='POST':
       '''    
        data = request.POST.copy()
        form = forms.AddUserForm(data)
  
        if form.is_valid():
  
            user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'],password = form.cleaned_data['password'],)
            user.is_active= False
            user.save()
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+user.username).hexdigest()
            key_expires=datetime.datetime.today() + datetime.timedelta(2)

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            userprofile = UserProfile(
                    user = user,
                    gender     = form.cleaned_data['gender'],
                    age = form.cleaned_data['age'],
                    branch = form.cleaned_data['branch'],
                    mobile_number = form.cleaned_data['mobile_number'],
#                    college =form.cleaned_data['college'],
                    college_roll = form.cleaned_data['college_roll'],
                    shaastra_id  = user.id , # is this right
                    activation_key = activation_key,
                    key_expires  = key_expires,
                    )
            userprofile.save()
            mail_template=get_template('email/activate.html')
            body = mail_template.render(Context({'username':user.username,
							 'SITE_URL':settings.SITE_URL,
							 'activationkey':userprofile.activation_key }))
            send_mail('Your new Shaastra2011 account confirmation', body,'noreply@shaastra.org', [user.email,], fail_silently=False)
            request.session['registered_user'] = True
        '''
    else:
        if request.user.get_profile().facebook_id :
            form = forms.AddUserForm(initial={'first_name':request.user.first_name,'last_name':request.user.last_name,'gender':request.user.get_profile().gender,'email':request.user.email,'username':request.user.get_profile().get_facebook_profile()['username'],})
        else:
             form = forms.AddUserForm()
#        coll_form = forms.AddCollegeForm(prefix="identifier")
    
#    registered_user = session_get(request,'registered_user')
    return render_to_response('register.html', locals(), context_instance= RequestContext(request))    

'''                           
def college_registration (request):
    if request.method == 'GET':
        data = request.GET.copy()
        coll_form = forms.AddCollegeForm(data,prefix="identifier")

        if coll_form.is_valid():
            college=coll_form.cleaned_data['name']
            if college.find('&')>=0:
                college = college.replace('&','and')
            city=coll_form.cleaned_data['city']
            state=coll_form.cleaned_data['state']
            
            if len (College.objects.filter(name=college, city=city, state=state))== 0 :
                college=College (name = college, city = city, state = state)
                college.save()
                data = college.name+","+college.city
                #return HttpResponse("created") 
                return HttpResponse(data, mimetype="text/plain")
            else:
                return HttpResponse("exists")
        else:
            return HttpResponse("failed")
    #redundant as registration done by ajax call....
    #else:
    #coll_form=forms.AddCollegeForm()        
    #return render_to_response('users/register_user.html', locals(), context_instance= global_context(request))        
            
def activate (request, a_key = None ): 
    """
       The activation_key (a_key) is trapped from the url. If the key is not empty then the corresponding userprofile object is retrieved. If the object doesn't exist and ObjectDoesNotExist error is flagged.
       
       The the key has already expired then the userprofile and the corresponding user objects are deleted, otherwise, the is_active field in the user model is set to true.
       
       Note that, if is_active is not set to true, the user cannot login. 
    """
    SITE_URL = settings.SITE_URL
    if (a_key == '' or a_key==None):
	    key_dne = True
    else:
        try:
	        user_profile = UserProfile.objects.get(activation_key = a_key)
        except ObjectDoesNotExist:
            prof_dne = True
        # try-except-else is actually there! God knows what for... Nested try blocks work just as well...
        else:
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
                user.save()
                request.session["registered"] = True
                activated = True
    return render_to_response('registration/activated.html',locals(), context_instance= global_context(request))
    
@needs_authentication
def myshaastra(request):
    user = request.user
    userprof = user.get_profile()
    events_list = userprof.registered
    return render_to_response('my_shaastra.html', locals(), context_instance = global_context(request))
    
@needs_authentication
def edit_profile(request):
    user = request.user
    userprofile = user.get_profile()
    form = forms.EditUserForm()
    if request.method=='POST':
        data=request.POST.copy()
        form=forms.EditUserForm(data)
        
        if form.is_valid():
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            #userprofile.age = form.cleaned_data['age']
            userprofile.college_roll=form.cleaned_data['college_roll']
            userprofile.mobile_number=form.cleaned_data['mobile_number']
            #userprofile.branch = form.cleaned_data['branch']
            userprofile.save()
            return HttpResponseRedirect ("%slogin/"%settings.SITE_URL)
    else:
        form=forms.EditUserForm(initial={'first_name':user.first_name, 'last_name':user.last_name, 'college_roll':userprofile.college_roll,'mobile_number':userprofile.mobile_number})
    return render_to_response('users/profile_update.html', locals(), context_instance= global_context(request))

def feedback(request):
    name, email = "", ""
    if request.user.is_authenticated():
        user = request.user
        name,email = user.first_name,user.email
    if request.method=='POST':
        data=request.POST.copy()
        feedback_list = [request.POST['graphics1'],request.POST['graphics2'],request.POST['graphics3'],request.POST['structure1'],request.POST['structure2'],request.POST['info1'],request.POST['info2'], request.POST['info3'], request.POST['gen1'],request.POST['gen2'],request.POST['gen3']]
        radiofeedbackstring = ''
        for i in feedback_list:
            radiofeedbackstring += '***___***'
            radiofeedbackstring += str(i)
        radiofeedbackstring += '***___***'
        feedbackstring = request.POST['gtext'] + "***___***"+ request.POST['stext'] + "***___***"+request.POST['text']
        newfeedback = models.Feedback ( name = request.POST['name'], email = request.POST['email'], content = feedbackstring, radiocontent = radiofeedbackstring )
        newfeedback.save()        
        return HttpResponseRedirect ("%shome/"%settings.SITE_URL)
    else:            
        return render_to_response('users/feedback.html', locals(), context_instance= global_context(request))        


def view_feedback(request):
    objs = models.Feedback.objects.all()
    ans = []
    for obj in objs:
        temp = []
        content = obj.content.split('***___***')
        radiocontent = obj.radiocontent.split('***___***')
        print content
        print radiocontent
        temp.append(radiocontent[0])
        temp.append(radiocontent[1])
        temp.append(radiocontent[2])
        temp.append(radiocontent[3])
        temp.append(content[0])
        temp.append(radiocontent[4])
        temp.append(radiocontent[5])
        temp.append(radiocontent[6])
        temp.append(radiocontent[7])
        temp.append(radiocontent[8])
        temp.append(content[1])
        temp.append(radiocontent[9])
        temp.append(content[2])
        temp.append(radiocontent[10])
        temp.append(radiocontent[11])
        ans.append(temp)
    return render_to_response('users/view_feedback.html', locals(), context_instance= global_context(request))        

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

def reset_password(request):
    if request.method == 'POST':
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user_id = form.cleaned_data['user']
            try:
                user = User.objects.get(pk = int(user_id))
                user.set_password(password)
                user.save()
                return HttpResponseRedirect('%smyshaastra/reset_password/done/' % settings.SITE_URL)
            except User.DoesNotExist:
                raise Http404
        return render_to_response('users/reset_password_form.html', locals(), context_instance = global_context(request))
    else:
        raise Http404

@needs_authentication
def show_profile(request):
    profile = request.user.get_profile()
    return render_to_response('users/show_profile.html', locals(), context_instance = global_context(request))
'''
