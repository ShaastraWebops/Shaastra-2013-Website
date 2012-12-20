#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from dajax.core import Dajax
from django.utils import simplejson
from django.template import loader, Context, RequestContext, Template
from events.models import *
from submissions.models import *
from coord.forms import *
from core.forms import AddEventForm
from dajaxice.decorators import dajaxice_register
from django.core.cache import cache
from django.contrib.sitemaps import ping_google
from operator import attrgetter


def get_files(tab):

    # gets all files that are related to a particular tab

    try:
        return tab.tabfile_set.all()
    except:
        raise Http404()


def get_mob_app_tab(event):
    try:
        return event.mobapptab
    except:
        return None


def get_tabs(event):

    # gets all tabs that are related to a particular event

    try:
        return event.tab_set.all()
    except:
        raise Http404()


@dajaxice_register
def edit_event(
    request,
    upload,
    form,
    id,
    ):
    """
    This function calls the AddEventForm from forms.py
    If a new event is being created, a blank form is displayed and the core can fill in necessary details.
    If an existing event's details is being edited, the same form is displayed populated with current event details for all fields

    """

    dajax = Dajax()
    event_form = AddEventForm(form, instance=Event.objects.get(id=id))
    if event_form.is_valid():
        event = event_form.save()
        try:
            ping_google()
        except:
            pass
        if upload:
            dajax.script('upload_events_logo(' + str(event.id) + ');')
        else:
            html = "<div class='right span2'><h2>" + event.category \
                + '<br>' + str(event) \
                + "</h2></div><div class='span2'><center><img src=" \
                + str(event.events_logo) + ' /></center></div>'
            dajax.assign('#eventdetails', 'innerHTML', html)
            dajax.script("window.location.hash='';")
    else:
        template = loader.get_template('ajax/core/editevent.html')
        html = template.render(RequestContext(request, locals()))
        dajax.assign('.bbq-item', 'innerHTML', html)
        dajax.script('load_add_tag();')
    return dajax.json()


@dajaxice_register
def updateTabs(request):
    """
    This function updates the tabs div
    """

    dajax = Dajax()
    event = request.user.get_profile().is_coord_of
    tabs = get_tabs(event)
    dajax.assign('#tabs', 'innerHTML', '')
    for tab in tabs:
        dajax.append('#tabs', 'innerHTML', '<li><a href='
                     + '#customtabs/' + str(tab.id) + ' name ='
                     + tab.title + ' id =' + str(tab.id) + ' >'
                     + tab.title + '</a></li> ')
    dajax.script("window.location.hash='';")
    return dajax.json()


@dajaxice_register
def add_tag(request, text):
    dajax = Dajax()
    if text:
        try:
            new_tag = Tag.objects.get(name=text)
            dajax.append('#alerts', 'innerHTML', "<li>'" + text
                         + "' already exists!</li>")
            dajax.assign('#addTag', 'innerHTML', '')
            dajax.script("$('#msg').show();")
        except:
            new_tag = Tag(name=text)
            new_tag.save()
            dajax.assign('#addTag', 'innerHTML', '')
            dajax.script("$('#msg').show();$('#id_tags option:last').attr('value',"
                          + str(new_tag.id)
                         + ");$('#id_tags').trigger('liszt:updated');")
    else:
        dajax.alert('Tag name required!')
    return dajax.json()


@dajaxice_register
def delete_tab(request, tab_id=0):

    # deletes the tab. shows a delete successful message.

    dajax = Dajax()
    if tab_id:
        tab = Tab.objects.get(id=tab_id)
        title = tab.title
        tab.delete()
        dajax.alert(title + ' deleted sucessfully!')
        dajax.script('Dajaxice.coord.updateTabs(Dajax.process);')
    else:
        dajax.alert('error ' + tab_id)
    return dajax.json()


@dajaxice_register
def save_tab(request, data, tab_id=0):

    # validates the tab details that were submitted while adding a new tab

    dajax = Dajax()
    if tab_id:
        tab = Tab.objects.get(id=tab_id)
        form = TabAddForm(data, instance=tab)
    else:
        form = TabAddForm(data)
    if form.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_tab = form.save(commit=False)
        unsaved_tab.event = event
        unsaved_tab.save()
        cache.set(str(unsaved_tab.id) + '_event',
                  str(unsaved_tab.event), 2592000)
        cache.set(str(unsaved_tab.id) + '_title',
                  str(unsaved_tab.title), 2592000)
        cache.set(str(unsaved_tab.id) + '_text', str(unsaved_tab.text),
                  2592000)
        cache.set(str(unsaved_tab.id) + '_pref', str(unsaved_tab.pref),
                  2592000)
        tab = unsaved_tab
        if not tab_id:
            dajax.append('#tabs', 'innerHTML', '<li><a href='
                         + '#customtabs/' + str(tab.id) + ' name ='
                         + str(tab.title) + ' id =' + str(tab.id)
                         + ' > ' + str(tab.title) + '  </a></li>')
        dajax.script("window.location.hash='" + 'customtabs/'
                     + str(tab.id) + "';")
        return dajax.json()
    else:
        template = loader.get_template('ajax/coord/tab_form.html')
        html = template.render(RequestContext(request, locals()))
        dajax.assign('.bbq-item', 'innerHTML', html)
        dajax.script("niced = new nicEditor().panelInstance('niced_text');"
                     )
        return dajax.json()


@dajaxice_register
def delete_file(request, tab_id, file_id):

    # deletes the selected file

    form = TabFile.objects.get(id=file_id)
    form.delete()
    tab = Tab.objects.get(id=tab_id)
    file_list = get_files(tab)
    template = loader.get_template('ajax/coord/tab_detail.html')
    html = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()


@dajaxice_register
def rename_file_done(request, form, file_id):

    # renames a file

    f = TabFile.objects.get(id=file_id)
    if form['display_name']:
        f.title = form['display_name']
        f.save()
    tab = f.tab
    file_list = get_files(tab)
    template = loader.get_template('ajax/coord/tab_detail.html')
    html = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()


@dajaxice_register
def save_subjective(request, data, ques_id=0):

    # validates and saves a subjective question

    dajax = Dajax()
    if ques_id:
        ques = SubjectiveQuestion.objects.get(id=ques_id)
        form = AddSubjectiveQuestionForm(data, instance=ques)
    else:
        form = AddSubjectiveQuestionForm(data)
    if form.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_ques = form.save(commit=False)
        unsaved_ques.event = event
        unsaved_ques.save()
        dajax.script("window.location.hash='questions'")
        return dajax.json()
    else:
        template = loader.get_template('ajax/coord/subj_form.html')
        html = template.render(RequestContext(request, locals()))
        dajax.assign('.bbq-item', 'innerHTML', html)
        dajax.script("niced = new nicEditor().panelInstance('niced_text');"
                     )
        return dajax.json()


@dajaxice_register
def delete_subjective(request, ques_id):

    # deletes the selected question

    ques = SubjectiveQuestion.objects.get(id=ques_id)
    ques.delete()
    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/coord/question_tab.html')
    html = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()


def saving_mcq(data, mcq):
    data.pop('csrfmiddlewaretoken')
    mcq.title = data.pop('title')
    mcq.q_number = data.pop('q_no')

#    print data

    mcq.save()
    try:
        options = mcq.mcqoption_set.all()
    except:
        options = []
    keys = data.keys()
    keys.sort()

#    print keys

    for opt_id in keys:
        if not data[opt_id]:
            continue
        if not opt_id.startswith('o'):

#            print 'not'
#            print opt_id[:-1]

            mcqoption = MCQOption(id=opt_id[:-1])
        else:

#            print 'h'
#            print 'else'

            mcqoption = MCQOption()

#            print 'here'

        mcqoption.option = opt_id[-1]
        mcqoption.text = data[opt_id]
        mcqoption.question = mcq
        mcqoption.save()


@dajaxice_register
def save_mcq(request, data, ques_id):
    mcq = \
        (ObjectiveQuestion.objects.get(id=ques_id) if ques_id else ObjectiveQuestion(event=request.user.get_profile().is_coord_of))
    saving_mcq(data, mcq)
    ques_id = mcq.id
    options = mcq.mcqoption_set.all()
    template = loader.get_template('ajax/coord/mcq_form.html')
    form = MCQForm(mcq, options)
    html = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.script("window.location.hash='questions'")
    dajax.script('alert("question saved succesfully");')
    return dajax.json()


@dajaxice_register
def delete_mcq(request, ques_id):

    # deletes the selected mcq

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    ques.delete()
    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/coord/question_tab.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def manage_options(request, ques_id):

    # all existing options displayed with features of editing/deleting them and adding new ones

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    options = ques.mcqoption_set.all()
    template = loader.get_template('ajax/coord/manage_options.html')
    html = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()


@dajaxice_register
def add_option(request, ques_id):

    # displays a form for adding an option

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    f = AddOptionForm()
    template = loader.get_template('ajax/coord/add_option_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#option_edit', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_option(request, form, ques_id):

    # validates and saves an option

    f = AddOptionForm(form)
    ques = ObjectiveQuestion.objects.get(id=ques_id)
    if f.is_valid():
        unsaved_option = f.save(commit=False)
        unsaved_option.question = ques
        unsaved_option.save()
        options = ques.mcqoption_set.all()
        template = loader.get_template('ajax/coord/manage_options.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = loader.get_template('ajax/coord/add_option_form.html'
                )
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#option_edit', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def delete_option(request, option_id):

    # deletes an option

    option = MCQOption.objects.get(id=option_id)
    ques = option.question
    option.delete()
    options = ques.mcqoption_set.all()
    template = loader.get_template('ajax/coord/manage_options.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def edit_option(request, option_id):

    # loads a form for editting an existing option

    option = MCQOption.objects.get(id=option_id)
    f = AddOptionForm(instance=option)
    template = loader.get_template('ajax/coord/edit_option_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#option_edit', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_editted_option(request, form, option_id):

    # validates and saves editted option

    option = MCQOption.objects.get(id=option_id)
    ques = option.question
    f = AddOptionForm(form, instance=option)
    if f.is_valid():
        f.save()
        options = ques.mcqoption_set.all()
        template = loader.get_template('ajax/coord/manage_options.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = \
            loader.get_template('ajax/coord/edit_option_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#option_edit', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def add_edit_mobapp_tab(request, form=''):
    dajax = Dajax()
    event = request.user.get_profile().is_coord_of
    mob_app_tab = get_mob_app_tab(event)
    template = loader.get_template('ajax/coord/add_edit_mobapptab.html')
    if mob_app_tab:
        f = MobAppWriteupForm(form, instance=mob_app_tab)
    else:
        f = MobAppWriteupForm(form)
    if f.is_valid():
        unsaved = f.save(commit=False)
        unsaved.event = event
        unsaved.save()
        dajax.alert('saved successfully!')
        dajax.script("window.location.hash='';")
    else:
        dajax.alert('Error. Your write up could not be saved!')
        t = template.render(RequestContext(request, locals()))
        dajax.assign('.bbq-item', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def add_edit_update(request, form='', id=0):
    dajax = Dajax()
    event = request.user.get_profile().is_coord_of
    initial = Update.objects.all()
    u_flag = 0
    a_flag = 0
    for u in initial:
        if u.event == event and u.category == 'Update' and u.expired \
            is False:
            u_flag = u_flag + 1
        elif u.event == event and u.category == 'Announcement' \
            and u.expired is False:
            a_flag = a_flag + 1
    if id:
        update_form = UpdateForm(form,
                                 instance=Update.objects.get(id=id))
    else:
        update_form = UpdateForm(form)
    if update_form.is_valid:
        update_temp = update_form.save(commit=False)
        update_temp.event = event
        if u_flag >= 4 and update_temp.category == 'Update' and not id:
            dajax.alert('This event already has 4 updates. Please mark atleast one update as Expired before adding a new update'
                        )
        elif a_flag >= 1 and update_temp.category == 'Announcement' and not id:

            dajax.alert('This event already has 1 announcement. Please mark the announcement as Expired before adding a new update'
                        )
        else:
            
            update_temp.save()
        dajax.assign('#updates', 'innerHTML', '<h4>Announcement</h4>')
        initial = Update.objects.all()
        update = sorted(initial, key=attrgetter('id'), reverse=True)
        for u in update:
            if u.event == event and u.category == 'Announcement' \
                and u.expired is False:
                dajax.append('#updates', 'innerHTML', '<p>' + u.subject
                             + ' - ' + u.description
                             + " <a style='float:right;' href="
                             + '#editupdate/' + str(u.id)
                             + " class='btn-mini btn-info atag'>Edit</a> "
                             )
        dajax.append('#updates', 'innerHTML', '<h4>Updates</h4>')
        for u in update:
            if u.event == event and u.category == 'Update' \
                and u.expired is False:
                dajax.append('#updates', 'innerHTML', '<p>' + u.subject
                             + ' - ' + u.description
                             + " <a style='float:right;' href="
                             + '#editupdate/' + str(u.id)
                             + " class='btn-mini btn-info atag'>Edit</a> "
                             )
        dajax.script("window.location.hash='';")
        dajax.script("$('.bbq-item').hide();$('.bbq-default').show();")
    else:
        template = loader.get_template('ajax/coord/update.html')
        t = template.render(RequestContext(request, locals()))
        dajax.assign('.bbq-item', 'innerHTML', t)
    return dajax.json()

def submission_list(request):
    dajax = Dajax()
    evt = request.user.get_profile().is_coord_of
    subs = TDPSubmissions.objects.filter(basesub__event = evt)
    template = \
        loader.get_template('ajax/submissions/all_tdp_submissions.html')
    html = template.render(RequestContext(request, locals()))
    dajax.assign('.bbq-item', 'innerHTML', html)
    dajax.script("$('#submissions_list').dataTable();")
    return dajax.json()

@dajaxice_register
def send_checklist(request,form=''):
    dajax = Dajax()
    assign = True
    if form['action'] == 'sub_read':
        assign = False
    if form['action'] == 'read':
        form['action'] = 'sub_read'
    try:
        for sub_id in form['sub_checklist']:
            sub = TDPSubmissions.objects.get(basesub__id = sub_id)
            setattr(sub.basesub, form['action'], assign)
            sub.basesub.save()
    except:
        sub_id = form['sub_checklist']
        sub = TDPSubmissions.objects.get(basesub__id = sub_id)
        setattr(sub.basesub, form['action'], assign)
        sub.basesub.save()       
    return submission_list(request)
