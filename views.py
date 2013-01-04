from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from users.models import UserProfile, Team
from events.models import Event, EVENT_CATEGORIES, Tag, Update, Sponsor
from django.template.defaultfilters import slugify
from events.views import home as events_home
from django.core.mail import send_mail
from django.template.loader import get_template
from forms import *

def home(request):
    fragment = request.GET.get('_escaped_fragment_','')
    splits = fragment.split('/')
    if fragment == 'hospi':
        return render_to_response('ajax/hospi_home.html',locals(),context_instance = RequestContext(request))
    elif fragment == 'spons':
        return render_to_response('ajax/spons_home.html',locals(),context_instance = RequestContext(request))
    elif splits[0] == 'events':
        return events_home(request)
    event_set=[]
    for c in EVENT_CATEGORIES :
        event_category_set = Event.objects.filter(category=c[0])
        if event_category_set :
            event_set.append(event_category_set)
            
    #Code for search
    result_list=[]
    for t in Tag.objects.all():
        row=[]
        row.append(str(t.name))
        temp=[]
        for x in t.event_set.all():
            url = slugify(x)
            temp.append([str(x),str(url)])
        row.append(temp)
        result_list.append(row)
    #End of search code
    # ading spons images code
    present_sponsors = Sponsor.objects.filter(year=2013).order_by('index_number')
    previous_sponsors = Sponsor.objects.filter(year=2011).order_by('index_number')
    previous_sponsors2 = Sponsor.objects.filter(year=2010).order_by('index_number')
    # end spons images
    # adding code for announcements on main page
    events = Event.objects.all()
    announcements = []
    for e in events:
      try:
        data = {'event':e,'announcement':Update.objects.get(event = e, category = "Announcement"),}
        announcements.append(data)
      except:
        pass
    # end announcements code
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif request.user.get_profile().is_core:
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif request.user.get_profile().is_coord_of:
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
        elif request.user.get_profile().is_hospi :
            return HttpResponseRedirect(settings.SITE_URL + 'controlroom/home')
        else:
            return render_to_response('index.html',locals(),context_instance = RequestContext(request))
    else:
        return render_to_response('index.html',locals(),context_instance = RequestContext(request))

def hospi(request):
    return render_to_response('hospi/hospi_home.html',locals(),context_instance = RequestContext(request))

def spons(request):
    present_sponsors = Sponsor.objects.filter(year=2013).order_by('index_number')
    previous_sponsors = Sponsor.objects.filter(year=2011).order_by('index_number')
    previous_sponsors2 = Sponsor.objects.filter(year=2010).order_by('index_number')
    return render_to_response('spons_home.html',locals(),context_instance = RequestContext(request))

def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404

def landing(request):
    return render_to_response('landing.html',locals(),context_instance = RequestContext(request))

def create(request):
    form = FileForm()    
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)   
        if form.is_valid():
            evt = Event.objects.get(id = form.cleaned_data['event_id'])
            line_number = 0
            for line in form.cleaned_data['files']:
                line = line.replace('\n', '').replace('\r', '')
                if line == '':
                    continue
                line_number += 1
                try:
                    new = User.objects.get(email = line)
                    if not evt.team_event:
                        try:
                            event = EventSingularRegistration.objects.get(user = new, event = evt)
                        except:
                            event = EventSingularRegistration(user = new, event = evt)
                            event.save()
                except:
                    try:
                        new = User.objects.get(username = line.split('@')[0].lower())
                    except:
                        new = User(
                                    username = line.split('@')[0].lower(),
                                    email = line
                                    )
                        new.set_password(line.split('@')[0].lower())
                        new.save()   
                        x = 1300000 + new.id 
                        new_profile = UserProfile(user = new,
                                       shaastra_id = ("SHA" + str(x)))
                        new_profile.save()
                        if not evt.team_event:
                            event = EventSingularRegistration(user = new, event = evt)
                            event.save()
                        msg = "Account created"
    return render_to_response('create_accounts.html', locals(),
                              context_instance=RequestContext(request))

def create_team(request):
    team_name = ''
    form = FileForm()    
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)   
        if form.is_valid():
            evt = Event.objects.get(id = form.cleaned_data['event_id'])
            line_number = 0
            for line in form.cleaned_data['files']:
                line = line.replace('\n','')
                if line == '':
                    continue
                line_number += 1
                new_team_name, member_email = line.split('\t')
                if not new_team_name == ' ':
                    team_name = new_team_name
                team = Team.objects.filter(name = team_name, event = evt)
                try:
                    user = User.objects.get(email = member_email)
                except User.DoesNotExist:
                    user = User(username = member_email.split('@')[0].lower(), email = member_email)
                    user.set_password(member_email.split('@')[0].lower())
                    try:
                        user.save()
                        x = 1300000 + user.id
                        new_profile = UserProfile(user = user, shaastra_id = ("SHA" + str(x)))
                        new_profile.save()
                    except:
                        user = User.objects.get(username = member_email.split('@')[0].lower())
                if not team:
                    team = Team(name = team_name, event = evt, leader = user)
                    team.save()
                    team.members.add(user)
                    team.save()
                elif user not in team[0].members.all():
                    team[0].members.add(user)
    return render_to_response('create_accounts.html', locals(), context_instance=RequestContext(request))

def create_hospi_accounts(request):
    userdetails = []
    form = FileForm()    
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)   
        if form.is_valid():
            line_number = form.cleaned_data['event_id']
            for line in form.cleaned_data['files']:
                line = line.replace('\n', '').replace('\r', '')
                if line == '':
                    continue
                line_number += 1
                new = User(
                            username = "dummy"+str(line_number),
                            email = "dummy"+str(line_number)+"@dummymail.com"
                            )
                new.set_password("dummyhospi"+str(line_number))
                new.save()   
                new_profile = UserProfile(user = new,
                                is_hospi = True)
                new_profile.save()
                userdetails.append(new)
                msg = "Account created"
    return render_to_response('create_accounts.html', locals(),
                              context_instance=RequestContext(request))
