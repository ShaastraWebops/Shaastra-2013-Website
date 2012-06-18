from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Template, Context, RequestContext
from dajax.core import Dajax
from admin.forms import *
from django.conf import settings
import os
from django.contrib.auth.models import Group

def get_template(file_name):
    #this is used to get templates from the path /.../shaastra/events/templates/events/ajax      (*in my case)
    #note - a separate folder for ajax templates.
    #this function opens files (*.html) and returns them as python string.
    filepath = os.path.join(settings.AJAX_TEMPLATE_DIR, file_name)
    f = open(filepath, mode='r')
    return f.read()

@dajaxice_register
def add_edit_group(request,form="",id=0):
    dajax = Dajax()
    if form == "" :
        if id:
            template = get_template('editgroup.html')
            group_form = AddGroupForm(instance=Group.objects.get(id=id))
            html=Template(template).render(RequestContext(request,locals()))
        else:
            template = get_template('addgroup.html')
            group_form = AddGroupForm()
            html=Template(template).render(RequestContext(request,locals()))
        dajax.assign('#space', 'innerHTML', html)
        return dajax.json()
    if id:
        group_form = AddGroupForm(form, instance=Group.objects.get(id=id))
    else:
        group_form = AddGroupForm(form)
    if group_form.is_valid():
        group_form.save()
    dajax.assign("#space",'innerHTML',"")
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def updateSummary(request):
    dajax = Dajax()
    dajax.assign("#summary",'innerHTML',"<table border='1'><thead><tr><th>S.No</th><th>Group Name</th></tr></thead><tbody id='groups'>")
    groups=Group.objects.order_by('id').all()
    for g in groups:
        dajax.append("#groups",'innerHTML',"<tr><td>"+str(g.id)+"</td><td onclick=\'displayGroup("+str(g.id)+");\' class='grps' id="+g.name+"><a href=#>"+g.name+"</a></td></tr>")
    return dajax.json()

@dajaxice_register
def del_group(request,id):
    dajax = Dajax()
    group=Group.objects.get(id=id)
    group.delete()
    dajax.assign('#space', 'innerHTML', "")
    dajax.script("updateSummary();")
    return dajax.json()

