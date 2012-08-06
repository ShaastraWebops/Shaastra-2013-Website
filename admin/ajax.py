#!/usr/bin/python
# -*- coding: utf-8 -*-
# The variable Summary refers to the div where a table consisting group name and its cores is displayed
# The variable space refers to the div where different forms like add/edit group/core are displayed

from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template import Context, RequestContext, loader
from dajax.core import Dajax
from admin.forms import *
from django.contrib.auth.models import Group, User
from users.models import UserProfile


@dajaxice_register
def add_edit_group(request, form='', id=0):
    """
    This function calls the AddGroupForm from forms.py
    If a new group is being created, a blank form is displayed and the super user can fill in necessary details.
    If an existing group's details is being edited, the same form is displayed populated with current group details for all fields

    """

    dajax = Dajax()
    if id:
        group_form = AddGroupForm(form,
                                  instance=Group.objects.get(id=id))
    else:
        group_form = AddGroupForm(form)
    if group_form.is_valid():
        group_form.save()
    dajax.script('updateSummary();')
    return dajax.json()


@dajaxice_register
def updateSummary(request):
    """
    This function updates the table in summary div whenever a new group/core is added or when an existing group/core is edited or deleted

    """

    dajax = Dajax()
    dajax.assign('#summary', 'innerHTML',
                 "<table border='1' class='table table-striped table-bordered table-condensed'><thead><tr><th>S.No</th><th>Group Name</th><th>Cores</th></tr></thead><tbody id='groups'>"
                 )
    groups = Group.objects.order_by('id').all()
    for g in groups:
        dajax.append('#groups', 'innerHTML', '<tr><td>' + str(g.id)
                     + "</td><td class='grps' id=" + g.name
                     + "><a class='tablelinks' href=" + '#editgroup/'
                     + str(g.id) + '/' + '>' + g.name
                     + '</a></td><td id=' + str(g.id) + '></td></tr>')
        cores = User.objects.filter(groups__name=g.name)
        for c in cores:
            if c.get_profile().is_core:
                dajax.append('#' + str(g.id), 'innerHTML',
                             "<li class='cores' id=" + str(c.username)
                             + "><a class='tablelinks' href="
                             + '#editcore/' + str(c.id) + '/' + '>'
                             + str(c) + '</a>')
    dajax.script("window.location.hash=''")
    return dajax.json()


@dajaxice_register
def del_group(request, id):
    """
    This function is called when the super user wants to delete a group

    """

    dajax = Dajax()
    group = Group.objects.get(id=id)
    group.delete()
    dajax.script('updateSummary();')
    return dajax.json()


@dajaxice_register
def add_edit_core(request, form='', id=0):
    """
    This function calls the AddCoreForm from forms.py
    If a new core is being created, a blank form is displayed and the super user can fill in necessary details.
    If an existing core's details is being edited, the same form is displayed populated with current core details for all fields

    """

    dajax = Dajax()
    if id:

        # groups field is a Many-to-Many field and requires a list of values

        grps = []
        grps.append(form['groups'])
        form['groups'] = grps
        core_form = AddCoreForm(form, instance=User.objects.get(id=id))
        if core_form.is_valid():
            core_form.save()
            dajax.script('updateSummary();')
        else:
            template = loader.get_template('ajax/admin/editcore.html')
            html = template.render(RequestContext(request, locals()))
            dajax.assign('.bbq-item', 'innerHTML', html)
    else:

        # groups field is a Many-to-Many field and requires a list of values

        grps = []
        grps.append(form['groups'])
        form['groups'] = grps
        core_form = AddCoreForm(form)
        if core_form.is_valid():
            core = core_form.save()
            core.set_password('default')
            core.save()
            core_profile = UserProfile(user=core, is_core=True)
            core_profile.save()
            dajax.script('updateSummary();')
        else:
            form['groups'] = grps[0]
            template = loader.get_template('ajax/admin/addcore.html')
            html = template.render(RequestContext(request, locals()))
            dajax.assign('.bbq-item', 'innerHTML', html)
            dajax.script("$('.chzn-select').chosen();")
    return dajax.json()


@dajaxice_register
def del_core(request, id):
    """
    This function is called when the super user wants to delete a core

    """

    dajax = Dajax()
    core = User.objects.get(id=id)
    core.delete()
    dajax.script('updateSummary();')
    return dajax.json()
