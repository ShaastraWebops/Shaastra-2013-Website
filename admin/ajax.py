from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Context, RequestContext, loader
from dajax.core import Dajax
from admin.forms import *
from django.contrib.auth.models import Group, User
from users.models import UserProfile

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
    dajax.assign("#summary",'innerHTML',"<table border='1'><thead><tr><th>S.No</th><th>Group Name</th><th>Cores</th></tr></thead><tbody id='groups'>")
    groups=Group.objects.order_by('id').all()
    for g in groups:
        dajax.append("#groups",'innerHTML',"<tr><td>"+str(g.id)+"</td><td onclick=\'displayGroup("+str(g.id)+");\' class='grps' id="+g.name+"><a href=#>"+g.name+"</a></td><td id="+str(g.id)+"></td></tr>")
        cores=User.objects.filter(groups__name=g.name)
        for c in cores:
            dajax.append("#"+str(g.id),'innerHTML',"<li onclick=\'displayCore("+str(c.id)+");\' class='cores' id="+str(c.username)+"><a href=#>"+str(c)+"</a>")
    return dajax.json()

@dajaxice_register
def del_group(request,id):
    dajax = Dajax()
    group=Group.objects.get(id=id)
    group.delete()
    dajax.assign('#space', 'innerHTML', "")
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def add_edit_core(request,form="",id=0):
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
    else:
        core_form = AddCoreForm(form)
    if core_form.is_valid():
        data = core_form.cleaned_data
        core_user=User(first_name = data['first_name'], last_name=data['last_name'], username= data['username'], email = data['email'])
        core_user.set_password(data['password'])
        core_user.save()
        grp=Group.objects.get(id=form['group'])
        grp.user_set.add(core_user)
        core_user.save()
        core_profile = UserProfile(
                user = core_user,
                gender = data['gender'],
                age = data['age'],
                mobile_number = data['mobile_number'],
                is_core=True,
                )
        core_profile.save()
        dajax.assign("#space",'innerHTML',"")
    else:
        dajax.prepend("#space",'innerHTML',"Enter valid details")
    dajax.script("updateSummary();")
    return dajax.json()

@dajaxice_register
def del_core(request,id):
    dajax = Dajax()
    core=User.objects.get(id=id)
    core.delete()
    dajax.assign('#space', 'innerHTML', "")
    dajax.script("updateSummary();")
    return dajax.json()

