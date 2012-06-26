import random
from dajax.core import Dajax
from django.utils import simplejson
from django.template import loader, Context, RequestContext, Template
from events.models import *
from dajaxice.decorators import dajaxice_register

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
    t1 = template.render(RequestContext(request,locals()))
    template = loader.get_template('events/tab_list.html')
    t2 = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t1)
    dajax.assign('#tabs','innerHTML', t2)
    return dajax.json()
        
@dajaxice_register
def confirm_delete_tab(request, tab_id):
    #asks coord 'are u sure u want to delete this tab?'
    tab = Tab.objects.get(id = tab_id)
    template = loader.get_template('events/tab_delete.html')
    t = template.render(RequestContext(request,locals()))
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
        template = loader.get_template('events/tab_list.html')
        t1 = template.render(RequestContext(request,locals()))
        template2 = loader.get_template('events/tab_detail.html')
        t2 = template2.render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#tabs','innerHTML', t1)
        dajax.assign('#detail', 'innerHTML', t2)
        return dajax.json()
    else:
        template = loader.get_template('events/tab_edit_form.html')
        t = template.render(RequestContext(request,locals()))
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
        template = loader.get_template('events/tab_list.html')
        t1 = template.render(RequestContext(request,locals()))
        template2 = loader.get_template('events/tab_detail.html')
        t2 = template2.render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#tabs','innerHTML', t1)
        dajax.assign('#detail', 'innerHTML', t2)
        return dajax.json()
    else:
        template = loader.get_template('events/tab_add_form.html')
        t = template.render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
        
@dajaxice_register
def add_tab(request):
    #loads a form for creating a new tab.
    f = TabAddForm()
    template = loader.get_template('events/tab_add_form.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def edit_tab(request, tab_id):
    #loads a form for editing the tab details.
    tab = Tab.objects.get(id = tab_id)
    f = TabAddForm(instance = tab)
    template = loader.get_template('events/tab_edit_form.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def load_tab(request, tab_id):
    #loads the tab details of the tab you clicked on.
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = loader.get_template('events/tab_detail.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()

@dajaxice_register
def add_file(request, tab_id):
    f = TabFileForm()
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = loader.get_template('events/file_form.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def delete_file(request, tab_id, file_id):
    f = TabFile.objects.get(id = file_id)
    f.delete()
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = loader.get_template('events/tab_detail.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()

@dajaxice_register
def rename_file(request, tab_id, file_id):
    tab = Tab.objects.get(id = tab_id)
    f = TabFile.objects.get(id = file_id)
    actual_name = f.tab_file.name.split('/')[-1]
    file_list = get_files(tab)
    template = loader.get_template('events/file_rename.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()    
        
@dajaxice_register
def rename_file_done(request, form, file_id):
    print 'here', form
    f = TabFile.objects.get(id = file_id)
    if form['display_name']:
        f.title = form['display_name']
        f.save()
    tab = f.tab
    file_list = get_files(tab)
    template = loader.get_template('events/tab_detail.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#detail','innerHTML', t)
    return dajax.json()    
        
        
