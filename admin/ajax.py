#The variable Summary refers to the div where a table consisting group name and its cores is displayed
#The variable space refers to the div where different forms like add/edit group/core are displayed

from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Context, RequestContext, loader
from dajax.core import Dajax
from admin.forms import *
from django.contrib.auth.models import Group, User
from users.models import UserProfile

@dajaxice_register
def add_edit_group(request,form="",id=0):
    """
    This function calls the AddGroupForm from forms.py
    If a new group is being created, a blank form is displayed and the super user can fill in necessary details.
    If an existing group's details is being edited, the same form is displayed populated with current group details for all fields

    """
    dajax = Dajax()
    if form == "" :
        if id:
            template = loader.get_template('ajax/admin/editgroup.html')
            group_form = AddGroupForm(instance=Group.objects.get(id=id))
            html=template.render(RequestContext(request,locals()))
        else:
            template = loader.get_template('ajax/admin/addgroup.html')
            group_form = AddGroupForm()
            html=template.render(RequestContext(request,locals()))
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
    """
    This function updates the table in summary div whenever a new group/core is added or when an existing group/core is edited or deleted

    """
    dajax = Dajax()
    dajax.assign("#summary",'innerHTML',"<table border='1'><thead><tr><th>S.No</th><th>Group Name</th><th>Cores</th></tr></thead><tbody id='groups'>")
    groups=Group.objects.order_by('id').all()[1:]
    for g in groups:
        dajax.append("#groups",'innerHTML',"<tr><td>"+str(g.id-1)+"</td><td onclick=\'displayGroup("+str(g.id)+");\' class='grps' id="+g.name+"><a href=#>"+g.name+"</a></td><td id="+str(g.id)+"></td></tr>")
        cores=User.objects.filter(groups__name=g.name)
        for c in cores:
            if c.get_profile().is_core:
	        dajax.append("#"+str(g.id),'innerHTML',"<li onclick=\'displayCore("+str(c.id)+");\' class='cores' id="+str(c.username)+"><a href=#>"+str(c)+"</a>")
    return dajax.json()

@dajaxice_register
def del_group(request,id):
    """
    This function is called when the super user wants to delete a group

    """
    dajax = Dajax()
    group=Group.objects.get(id=id)
    group.delete()
    dajax.assign('#space', 'innerHTML', "")
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def add_edit_core(request,form="",id=0):
    """
    This function calls the AddCoreForm from forms.py
    If a new core is being created, a blank form is displayed and the super user can fill in necessary details.
    If an existing core's details is being edited, the same form is displayed populated with current core details for all fields

    """
    dajax = Dajax()
    if form == "" :
        if id:
            template = loader.get_template('ajax/admin/editcore.html')
            core_form = AddCoreForm(instance=User.objects.get(id=id))
            html=template.render(RequestContext(request,locals()))
        else:
            template = loader.get_template('ajax/admin/addcore.html')
            core_form = AddCoreForm()
            html=template.render(RequestContext(request,locals()))
        dajax.assign('#space', 'innerHTML', html)
        return dajax.json()
    if id:
        core_form = AddCoreForm(form, instance=User.objects.get(id=id))
        if core_form.is_valid():
            core_form.save()
            dajax.assign("#space",'innerHTML',"")
        else:
            template = loader.get_template('ajax/admin/editcore.html')
            html=template.render(RequestContext(request,locals()))
            dajax.assign("#space",'innerHTML',html)
    else:
        core_form = AddCoreForm(form)
        if core_form.is_valid():
            core=core_form.save()
            core.set_password("default")
            core.save()
            core_profile = UserProfile( user=core, is_core=True)
            core_profile.save()
            dajax.assign("#space",'innerHTML',"")
        else:
            template = loader.get_template('ajax/admin/addcore.html')
            html=template.render(RequestContext(request,locals()))
            dajax.assign("#space",'innerHTML',html)
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def del_core(request,id):
    """
    This function is called when the super user wants to delete a core

    """
    dajax = Dajax()
    core=User.objects.get(id=id)
    core.delete()
    dajax.assign('#space', 'innerHTML', "")
    dajax.script("updateSummary();")
    return dajax.json()