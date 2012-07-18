#The variable Summary refers to the div where a table consisting event name and its coords is displayed
#The variable space refers to the div where different forms like add/edit event/coord are displayed

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
    dajax.assign("#summary",'innerHTML',"<table border='1' class='table table-striped table-bordered table-condensed'><thead><tr><th>S.No</th><th>Event Name</th><th>Coords</th></tr></thead><tbody id='event'>")
    event=Event.objects.order_by('id').all()
    for e in event:
        dajax.append("#event",'innerHTML',"<tr><td>"+str(e.id)+"</td><td id="+e.title+"><a href="+'dashboard/'+str(e.id)+">"+e.title+"</a><button class='btn btn-primary' onclick='del_event("+str(e.id)+");' >Delete</button></td><td id="+str(e.id)+"></td></tr>")
        coords=UserProfile.objects.filter(is_coord_of__title=e.title)
        coords=coords.filter(is_core=0)
        for c in coords:
            dajax.append("#"+str(e.id),'innerHTML',"<li class='coords' id="+str(c.user.username)+"><a href="+'#editcoord/'+str(c.user_id)+">"+str(c.user)+"</a>")
    dajax.script("window.location.hash=''")
    return dajax.json()

@dajaxice_register
def add_event(request,upload,form):
    """
    This function calls the AddEventForm from forms.py
    If a new event is being created, a blank form is displayed and the core can fill in necessary details.
    If an existing event's details is being edited, the same form is displayed populated with current event details for all fields

    """
    dajax = Dajax()
    event_form = AddEventForm(form)
    if event_form.is_valid():
        event = event_form.save()
        if upload :
	    dajax.script("upload_events_logo(" + str(event.id) + ");")
	else:
	    dajax.script("updateSummary();")
    else:
	template = loader.get_template('ajax/core/addevent.html')
        html=template.render(RequestContext(request,locals()))
        dajax.assign(".bbq-item",'innerHTML',html)
    return dajax.json()

@dajaxice_register
def del_event(request,id):
    """
    This function is called when the core wants to delete an event

    """
    dajax = Dajax()
    event=Event.objects.get(id=id)
    event.delete()
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def add_edit_coord(request,form="",id=0):
    """
    This function calls the AddCoordForm from forms.py
    If a new coord is being created, a blank form is displayed and the core can fill in necessary details.
    If an existing coord's details is being edited, the same form is displayed populated with current coord details for all fields

    """
    dajax = Dajax()
    if id:
        coord_form = AddCoordForm(form, instance=User.objects.get(id=id))
        if coord_form.is_valid():
            coord=coord_form.save()
            coord_profile=coord.get_profile()
            coord_profile.is_coord_of_id=form['event']
            coord_profile.save()
            dajax.script("updateSummary();")
        else:
            template = loader.get_template('ajax/core/editcoord.html')
            html=template.render(RequestContext(request,locals()))
            dajax.assign(".bbq-item",'innerHTML',html)
    else:
        coord_form = AddCoordForm(form)
        if coord_form.is_valid():
            coord=coord_form.save()
            coord.set_password("default")
            coord.groups.add(request.user.groups.get_query_set()[0])
            coord.save()
            coord_profile = UserProfile(user=coord, is_coord_of_id=form['event'])
            coord_profile.save()
            dajax.script("updateSummary();")
        else:
            template = loader.get_template('ajax/core/addcoord.html')
            html=template.render(RequestContext(request,locals()))
            dajax.assign(".bbq-item",'innerHTML',html)
    return dajax.json()

@dajaxice_register
def del_coord(request,id):
    """
    This function is called when the core wants to delete a coord

    """
    dajax = Dajax()
    coord=User.objects.get(id=id)
    coord.delete()
    dajax.script("updateSummary();")
    return dajax.json()