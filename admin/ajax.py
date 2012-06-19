from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Context, RequestContext, loader
from dajax.core import Dajax
from admin.forms import *
from django.contrib.auth.models import Group

@dajaxice_register
def add_edit_group(request,form="",id=0):
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

