import random
from dajax.core import Dajax
from django.utils import simplejson
from django.template import Template,Context, RequestContext
from events.models import *
from dajaxice.decorators import dajaxice_register
from django.conf import settings
import os

def get_template(file_name):
    #this is used to get templates from the path /.../shaastra/events/templates/events/ajax      (*in my case)
    #note - a separate folder for ajax templates.
    #this function opens files (*.html) and returns them as python string.
    filepath = os.path.join(settings.AJAX_TEMPLATE_DIR, file_name)
    f = open(filepath, mode='r')
    return f.read()

def get_files(tab):
    try:
        return tab.tabfile_set.all()
    except:
        print 'here too'
        raise Http404()

def get_tabs(event):
    try:
        return event.tab_set.all()
    except:
        print 'here'
        raise Http404()

@dajaxice_register
def save_file(request, form, tab_id):
    print 'here'
    print form
    print tab_id
    dajax = Dajax()
    return dajax.json()
        
@dajaxice_register
def delete_tab(request, tab_id):
    #deletes the tab. shows a delete successful message.
    tab = Tab.objects.get(id = tab_id)
    x = tab.title
    tab.delete()
    event = request.user.get_profile().is_coord_of
    tabs = get_tabs(event)
    template = """{{x}} deleted successfully!"""
    t1 = Template(template).render(RequestContext(request,locals()))
    template = get_template('tab_list.html')
    t2 = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t1)
    dajax.assign('#tabs','innerHTML', t2)
    return dajax.json()
        
@dajaxice_register
def confirm_delete_tab(request, tab_id):
    #asks coord 'are u sure u want to delete this tab?'
    tab = Tab.objects.get(id = tab_id)
    template = get_template('tab_delete.html')
    t = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()
        
@dajaxice_register
def save_editted_tab(request, form, tab_id):
    #validates the tab details that were submitted while editing an existing tab
    tab = Tab.objects.get(id = tab_id)
    f = TabAddForm(form, instance = tab)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_tab = f.save(commit = False)
        unsaved_tab.event = event
        unsaved_tab.save()
        tab = unsaved_tab
        tabs = get_tabs(event)
        template = get_template('tab_list.html')
        t1 = Template(template).render(RequestContext(request,locals()))
        template2 = get_template('tab_detail.html')
        t2 = Template(template2).render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#tabs','innerHTML', t1)
        dajax.assign('#detail', 'innerHTML', t2)
        return dajax.json()
    else:
        template = get_template('tab_edit_form.html')
        t = Template(template).render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()

@dajaxice_register
def save_tab(request, form):
    #validates the tab details that were submitted while adding a new tab.
    f = TabAddForm(form)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_tab = f.save(commit = False)
        unsaved_tab.event = event
        unsaved_tab.save()
        tab = unsaved_tab
        tabs = get_tabs(event)
        template = get_template('tab_list.html')
        t1 = Template(template).render(RequestContext(request,locals()))
        template2 = get_template('tab_detail.html')
        t2 = Template(template2).render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#tabs','innerHTML', t1)
        dajax.assign('#detail', 'innerHTML', t2)
        return dajax.json()
    else:
        template = get_template('tab_add_form.html')
        t = Template(template).render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
        
@dajaxice_register
def add_tab(request):
    #loads a form for creating a new tab.
    f = TabAddForm()
    template = get_template('tab_add_form.html')
    t = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def edit_tab(request, tab_id):
    #loads a form for editing the tab details.
    tab = Tab.objects.get(id = tab_id)
    f = TabAddForm(instance = tab)
    template = get_template('tab_edit_form.html')
    t = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def load_tab(request, tab_id):
    #loads the tab details of the tab you clicked on.
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = get_template('tab_detail.html')
    t = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()

@dajaxice_register
def add_file(request, tab_id):
    f = TabFileForm()
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = get_template('file_form.html')
    t = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def delete_file(request, tab_id, file_id):
    f = TabFile.objects.get(id = file_id)
    f.delete()
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = get_template('tab_detail.html')
    t = Template(template).render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()

#this needs to be done
@dajaxice_register
def rename_file(request, tab_id, file_id):
    dajax = Dajax()
    return dajax.json()    
        
        
