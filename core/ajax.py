from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Context, RequestContext, loader
from dajax.core import Dajax
from core.forms import *
from events.models import Event

@dajaxice_register
def add_edit_event(request,form="",id=0):
    dajax = Dajax()
    if form == "" :
        if id:
            template = loader.get_template('ajax/core/editevent.html')
            event_form = AddEventForm(instance=Event.objects.get(id=id))
            html=template.render(RequestContext(request,locals()))
        else:
            template = loader.get_template('ajax/core/addevent.html')
            event_form = AddEventForm()
            html=template.render(RequestContext(request,locals()))
        dajax.assign('#space', 'innerHTML', html)
        return dajax.json()
    if id:
        event_form = AddEventForm(form, instance=Event.objects.get(id=id))
    else:
        event_form = AddEventForm(form)
    if event_form.is_valid():
        event_form.save()
    dajax.assign("#space",'innerHTML',"")
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def updateSummary(request):
    dajax = Dajax()
    dajax.assign("#summary",'innerHTML',"<table border='1'><thead><tr><th>S.No</th><th>Event Name</th></tr></thead><tbody id='events'>")
    events=Event.objects.order_by('id').all()
    for g in events:
        dajax.append("#events",'innerHTML',"<tr><td>"+str(g.id)+"</td><td onclick=\'displayevent("+str(g.id)+");\' class='grps' id="+g.title+"><a href=#>"+g.title+"</a></td></tr>")
    return dajax.json()

@dajaxice_register
def del_event(request,id):
    dajax = Dajax()
    event=Event.objects.get(id=id)
    event.delete()
    dajax.assign('#space', 'innerHTML', "")
    dajax.script("updateSummary();")
    return dajax.json()

