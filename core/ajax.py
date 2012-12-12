#!/usr/bin/python
# -*- coding: utf-8 -*-
# The variable Summary refers to the div where a table consisting event name and its coords is displayed
# The variable space refers to the div where different forms like add/edit event/coord are displayed

from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Context, RequestContext, loader
from dajax.core import Dajax
from core.forms import *
from events.models import Event
from django.contrib.auth.models import User
from users.models import UserProfile


@dajaxice_register
def updateSummary(request):
    """
    This function updates the table in summary div whenever a new event/coord is added or when an existing event/coord is edited or deleted

    """

    dajax = Dajax()
    dajax.assign('#summary', 'innerHTML',
                 "<table border='1' class='table table-striped table-bordered table-condensed'><thead><tr><th>S.No</th><th>Event Name</th></tr></thead><tbody id='event'>"
                 )
    event = Event.objects.order_by('id').all()
    for e in event:
        dajax.append('#event', 'innerHTML', '<tr><td>' + str(e.id)
                     + '</td><td id=' + e.title
                     + "><a class='tablelinks left' href="
                     + 'dashboard/' + str(e.id) + '>' + e.title
                     + "</a><button class='btn btn-primary right' onclick='del_event("
                      + str(e.id) + ");' >Delete</button></td></tr>")
    dajax.script("window.location.hash=''")
    return dajax.json()


@dajaxice_register
def add_event(request, form):
    """
    This function calls the AddEventForm from forms.py
    If a new event is being created, a blank form is displayed and the core can fill in necessary details.
    If an existing event's details is being edited, the same form is displayed populated with current event details for all fields

    """

    dajax = Dajax()
    try:
        tags = []
        tags.append(form['tags'])
        form['tags'] = tags
    except:
        pass
    event_form = AddEventForm(form)
    if event_form.is_valid():
        event = event_form.save()
        user_name = event.title.replace(' ', '_')
        new_user = User(username=user_name, email=user_name
                        + '@shaastra.org')
        new_user.set_password('default')
        new_user.save()
        userprofile = UserProfile(user=new_user, is_coord_of=event)
        userprofile.save()
        dajax.script('updateSummary();')
    else:
        template = loader.get_template('ajax/core/addevent.html')
        html = template.render(RequestContext(request, locals()))
        dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()


@dajaxice_register
def del_event(request, id):
    """
    This function is called when the core wants to delete an event

    """

    dajax = Dajax()
    event = Event.objects.get(id=id)
    user_name = event.title.replace(' ', '_')
    user = User.objects.get(username=user_name)
    userprofile = UserProfile.objects.get(user=user)
    userprofile.delete()
    user.delete()
    event.delete()
    dajax.script('updateSummary();')
    return dajax.json()
