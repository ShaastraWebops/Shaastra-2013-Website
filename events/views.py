#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from events.models import *
from users.models import Team
from operator import attrgetter
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
import urllib


# Create your views here.
def home(request):
    events = Event.objects.all()
    initial_updates = Update.objects.filter(category = 'Update')
    updates = sorted(initial_updates, key=attrgetter('id'), reverse=True)
    initial_announcements = Update.objects.filter(category = 'Announcement')
    announcements = sorted(initial_announcements, key=attrgetter('id'), reverse=True)
    return render_to_response('events/events_home.html', locals(), context_instance=RequestContext(request))

def events(request, event_name):
    event_name = event_name.replace('-', ' ')
    if event_name=="robo oceana":
    	event_name="robo-oceana"
    elif event_name=="lectures video conferences":
    	event_name="lectures & video conferences"
    if event_name == 'sampark/' :
        return sampark(request)
    event = Event.objects.get(title=event_name)
    initial_updates = Update.objects.filter(category = 'Update')
    updates = sorted(initial_updates, key=attrgetter('id'), reverse=True)
    initial_announcements = Update.objects.filter(category = 'Announcement')
    announcements = sorted(initial_announcements, key=attrgetter('id'), reverse=True)
    tab_set = event.tab_set.all()
    files_set = [tab.tabfile_set.all() for tab in tab_set]
    tabs = zip(tab_set,files_set)
    #assert False
    return render_to_response('events/events.html', locals(), context_instance=RequestContext(request))

'''
def tabs(request, event_name, tab_name):
    event_name = event_name.replace('-', ' ')
    tab_name = tab_name.replace('-', ' ')
    if event_name=="robo oceana":
    	event_name="robo-oceana"
    elif event_name=="lectures video conferences":
    	event_name="lectures & video conferences"
    event = Event.objects.get(title=event_name)
    tab_set = event.tab_set.all()
    tab = tab_set.get(title=tab_name)
    file_set = tab.tabfile_set.all()
    return render_to_response('events/tabs.html', locals(), context_instance=RequestContext(request))
'''
def sampark(request):
#    if path:
#        assert False
#        return HttpResponseRedirect(settings.SITE_URL+path)
    bengaluruevents = []
    hyderabadevents = []
    puneevents = []
    coimbatoreevents = []
    chennaievents = []
    event = Event.objects.all()
    city_set = ['Bengaluru', 'Hyderabad', 'Coimbatore', 'Pune', 'Chennai']
    for e in event:
        if e.title.split('_')[0] == 'B':
            bengaluruevents.append(e)
        if e.title.split('_')[0] == 'H':
            hyderabadevents.append(e)
        if e.title.split('_')[0] == 'P':
            puneevents.append(e)
        if e.title.split('_')[0] == 'C':
            coimbatoreevents.append(e)
        if e.title.split('_')[0] == 'Ch':
            chennaievents.append(e)
    #Code for search
    result_list=[]
    for t in Tag.objects.all():
        row=[]
        row.append(str(t.name))
        temp=[]
        for x in t.event_set.all():
            url = slugify(x) + '/tab/' + x.tab_set.all()[0].title
            temp.append([str(x),str(url)])
        row.append(temp)
        result_list.append(row)
    #End of search code
    return render_to_response('events/sampark_home.html', locals(), context_instance=RequestContext(request))

def logo(request):
    event_name = request.GET.get('event_name','')
    spons_logo_url = request.GET.get('url','')
    event = Event.objects.get(title=event_name)
    event.sponsor_logo_url = spons_logo_url
    event.save()
    event = Event.objects.get(title=event_name)
    return HttpResponse("True")
    

### Methods for event registration:
        
def register_singular_event(request, event):
    user = request.user
    userProfile = user.get_profile()
    singularRegistrations = EventSingularRegistration.objects.filter(event = event)
    registration_done_message = None
    try:
        userRegistration = singularRegistrations.get(user = user)
    except:
        # This means that the user is not registered.
        # We must now execute the registration logic.
        if request.method == 'POST':
            # If the user submitted the registration form (which is just a confirm button)
            newRegistration = EventSingularRegistration(user = user, event = event)
            newRegistration.save()
            registration_done_message = u'You have been registered for this event.'
        else:
            # If the form has not been submitted, we have to render the form.
            # TODO: The template below should have a form which allows the user to choose whether he wants to register or not. TODO done
            return render_to_response('events/register_singular_event.html', locals(), context_instance=RequestContext(request))
    if registration_done_message is None:
        # If registration_done_message exists, then the user just registered. Do not change this message here.
        # If it does not exist, the user registered earlier. Set the message.
        registration_done_message = u'You have already registered for this event.'
    # TODO: The template below should tell the user that he is registered. TODO done
    # TODO: The template should also allow the user to cancel his registration
    return render_to_response('events/registration_done.html', locals(), context_instance=RequestContext(request))

def register_team_event(request, event):
    user = request.user
    userProfile = user.get_profile()
    teams = Team.objects.filter(event = event)
    try:
        userTeam = teams.get(members = user)
    except Team.DoesNotExist:
        # This means that the user is not a part of any registered team.
        # We must now execute the team registration logic.
        # To register for an event, the user must create a team.
        # If the user wants to join another team, the leader of that team must send the user a request.
        # Here we must redirect to the create team view.
        return render_to_response('events/team_registration_required.html', locals(), context_instance=RequestContext(request))
        #return HttpResponseRedirect(settings.SITE_URL + 'user/teams/create/' + str(event.id) + '/')
    # Else the user is already part of a team.
    return render_to_response('events/team_registration_done.html', locals(), context_instance=RequestContext(request))

@login_required
def register(request, event_id):
    """ 
    This is the event registration view.
    If the event is a singular event, i.e. individual participation, the
    user will be shown a form asking him to register.
    If the event is a team event, the user will be redirected to the team
    selection page
    """
    event_id = int(event_id)
    try:
        event = Event.objects.get(id = event_id)
    except Event.DoesNotExist:
        raise Http404('It seems like you the event you have requested for does not exist.')
    if not event.registrable_online:
        return render_to_response('events/register_offline.html', locals(), context_instance=RequestContext(request))
        #TODO: This template should tell the user that the event cannot be registered for online and that the registration is only on site. TODO done
    if not event.begin_registration:
        return render_to_response('events/registration_not_started.html', locals(), context_instance=RequestContext(request))
        #TODO: This template should tell the user that the event registration is online but has not started yet. Stay tuned for updates. TODO done
    if not event.team_event:  # This means that the event is a singular event.
        response = register_singular_event(request, event)
        return response
    else:  # The event is a team event.
        response = register_team_event(request, event)
        return response

@login_required        
def cancel_registration(request, event_id):
    """
    This view cancels a users registration for an event.
    """
    event_id = int(event_id)
    user = request.user
    try:
        event = Event.objects.get(id = event_id)
    except Event.DoesNotExist:
        raise Http404('It seems like you the event you have requested for does not exist.')
    if event.team_event:
        # TODO: This template should tell the user how to deregister from a team event TODO done
        return render_to_response('events/team_deregister.html', locals(), context_instance=RequestContext(request))
    try:
        user_registration = EventSingularRegistration.objects.filter(event=event).get(user=user)
    except:
        raise Http404('You are not registered for this event.')
    
    if request.method == 'POST':
        # If the user submitted the registration cancellation form (which is just a confirm button)
        user_registration.delete()
        return render_to_response('events/deregistration_done.html', locals(), context_instance=RequestContext(request))
    else:
        # If the form has not been submitted, we have to render the form.
        # TODO: The template below should have a form which allows the user to choose whether he wants to cancel registration or not. TODO done
        return render_to_response('events/deregister_singular_event.html', locals(), context_instance=RequestContext(request))

