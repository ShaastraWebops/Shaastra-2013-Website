#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from dajax.core import Dajax
from django.utils import simplejson
from django.template import loader, Context, RequestContext, Template
from events.models import *
from dajaxice.decorators import dajaxice_register
from django.core.cache import cache


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
def delete_tab(request, tab_id):

    # deletes the tab. shows a delete successful message.

    tab = Tab.objects.get(id=tab_id)
    x = tab.title
    tab.delete()
    event = request.user.get_profile().is_coord_of
    tabs = get_tabs(event)
    template = """{{x}} deleted successfully!"""
    t1 = Template(template).render(RequestContext(request, locals()))
    template = loader.get_template('ajax/events/tab_list.html')
    t2 = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t1)
    dajax.assign('#tabs', 'innerHTML', t2)
    return dajax.json()


@dajaxice_register
def confirm_delete_tab(request, tab_id):

    # asks coord 'are u sure u want to delete this tab?'

    tab = Tab.objects.get(id=tab_id)
    template = loader.get_template('ajax/events/tab_delete.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_editted_tab(request, form, tab_id):

    # validates the tab details that were submitted while editing an existing tab

    tab = Tab.objects.get(id=tab_id)
    f = TabAddForm(form, instance=tab)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_tab = f.save(commit=False)
        unsaved_tab.event = event
        unsaved_tab.save()
        tab = unsaved_tab
        tabs = get_tabs(event)
        template = loader.get_template('ajax/events/tab_list.html')
        t1 = template.render(RequestContext(request, locals()))
        template2 = loader.get_template('ajax/events/tab_detail.html')
        t2 = template2.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#tabs', 'innerHTML', t1)
        dajax.assign('#detail', 'innerHTML', t2)
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/tab_edit_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def save_tab(request, form):

    # validates the tab details that were submitted while adding a new tab

    f = TabAddForm(form)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_tab = f.save(commit=False)
        unsaved_tab.event = event
        unsaved_tab.save()
        tab = unsaved_tab
        tabs = get_tabs(event)
        template = loader.get_template('ajax/events/tab_list.html')
        t1 = template.render(RequestContext(request, locals()))
        template2 = loader.get_template('ajax/events/tab_detail.html')
        t2 = template2.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#tabs', 'innerHTML', t1)
        dajax.assign('#detail', 'innerHTML', t2)
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/tab_add_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def add_tab(request):

    # loads a form for creating a new tab

    f = TabAddForm()
    template = loader.get_template('ajax/events/tab_add_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def edit_tab(request, tab_id):

    # loads a form for editing the tab details

    tab = Tab.objects.get(id=tab_id)
    f = TabAddForm(instance=tab)
    template = loader.get_template('ajax/events/tab_edit_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def load_tab(request, tab_id):

    # loads the tab details of the tab you clicked on

    event_name = cache.get(str(tab_id) + '_event')
    if event_name != None:
        event = Event.objects.get(title=event_name)
        title = cache.get(str(tab_id) + '_title')
        text = cache.get(str(tab_id) + '_text')
        pref = cache.get(str(tab_id) + '_pref')
        tab = Tab(event=event, title=title, text=text, pref=int(pref))
    else:
        tab = Tab.objects.get(id=tab_id)
        cache.set(str(unsaved_tab.id) + '_event',
                  str(unsaved_tab.event), 2592000)
        cache.set(str(unsaved_tab.id) + '_title',
                  str(unsaved_tab.title), 2592000)
        cache.set(str(unsaved_tab.id) + '_text', str(unsaved_tab.text),
                  2592000)
        cache.set(str(unsaved_tab.id) + '_pref', str(unsaved_tab.pref),
                  2592000)
    file_list = get_files(tab)
    template = loader.get_template('ajax/events/tab_detail.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def add_file(request, tab_id):

    # loads a form for adding files inside a tab

    f = TabFileForm()
    tab = Tab.objects.get(id=tab_id)
    file_list = get_files(tab)
    template = loader.get_template('ajax/events/file_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def delete_file(request, tab_id, file_id):

    # deletes the selected file

    f = TabFile.objects.get(id=file_id)
    f.delete()
    tab = Tab.objects.get(id=tab_id)
    file_list = get_files(tab)
    template = loader.get_template('ajax/events/tab_detail.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def rename_file(request, tab_id, file_id):

    # loads a form for renaming a file

    tab = Tab.objects.get(id=tab_id)
    f = TabFile.objects.get(id=file_id)
    actual_name = f.tab_file.name.split('/')[-1]
    file_list = get_files(tab)
    template = loader.get_template('ajax/events/file_rename.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
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
    template = loader.get_template('ajax/events/tab_detail.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def load_question_tab(request):

    # question tab is displayed

    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/events/question_tab.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def add_subjective(request):

    # loads a form for creating a new subjective question.

    f = AddSubjectiveQuestionForm()
    template = \
        loader.get_template('ajax/events/add_subjective_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_subjective(request, form):

    # validates and saves a subjective question

    from django.conf import settings
    f = AddSubjectiveQuestionForm(form)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_ques = f.save(commit=False)
        unsaved_ques.event = event
        unsaved_ques.save()
        text_questions = event.subjectivequestion_set.all()
        mcqs = event.objectivequestion_set.all()
        template = loader.get_template('ajax/events/question_tab.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = \
            loader.get_template('ajax/events/add_subjective_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def edit_subjective(request, ques_id):

    # loads a form for editing the selected question

    ques = SubjectiveQuestion.objects.get(id=ques_id)
    f = AddSubjectiveQuestionForm(instance=ques)
    template = \
        loader.get_template('ajax/events/edit_subjective_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_editted_subjective(request, form, ques_id):

    # validates the question details that were submitted while editing an existing question.

    ques = SubjectiveQuestion.objects.get(id=ques_id)
    f = AddSubjectiveQuestionForm(form, instance=ques)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_ques = f.save(commit=False)
        unsaved_ques.event = event
        unsaved_ques.save()
        text_questions = event.subjectivequestion_set.all()
        mcqs = event.objectivequestion_set.all()
        template = loader.get_template('ajax/events/question_tab.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = \
            loader.get_template('ajax/events/edit_subjective_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def delete_subjective(request, ques_id):

    # deletes the selected question

    ques = SubjectiveQuestion.objects.get(id=ques_id)
    ques.delete()
    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/events/question_tab.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def add_mcq(request):

    # loads a form for creating a new mcq question.

    f = AddMCQForm()
    template = loader.get_template('ajax/events/add_mcq_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_mcq(request, form):

    # validates and saves the mcq and displays a page to manage options

    from django.conf import settings
    f = AddMCQForm(form)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        ques = f.save(commit=False)
        ques.event = event
        ques.save()
        template = loader.get_template('ajax/events/manage_options.html'
                )
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/add_mcq_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def edit_mcq(request, ques_id):

    # loads a form for editing the selected mcq

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    f = AddMCQForm(instance=ques)
    template = loader.get_template('ajax/events/edit_mcq_form.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def save_editted_mcq(request, form, ques_id):

    # validates the question details that were submitted while editing an existing mcq and displays a page to manage options

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    f = AddMCQForm(form, instance=ques)
    if f.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_ques = f.save(commit=False)
        unsaved_ques.event = event
        unsaved_ques.save()
        options = unsaved_ques.mcqoption_set.all()
        template = loader.get_template('ajax/events/manage_options.html'
                )
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/edit_mcq_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def delete_mcq(request, ques_id):

    # deletes the selected mcq

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    ques.delete()
    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/events/question_tab.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def manage_options(request, ques_id):

    # all existing options displayed with features of editing/deleting them and adding new ones

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    options = ques.mcqoption_set.all()
    template = loader.get_template('ajax/events/manage_options.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def add_option(request, ques_id):

    # displays a form for adding an option

    ques = ObjectiveQuestion.objects.get(id=ques_id)
    f = AddOptionForm()
    template = loader.get_template('ajax/events/add_option_form.html')
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
        template = loader.get_template('ajax/events/manage_options.html'
                )
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = \
            loader.get_template('ajax/events/add_option_form.html')
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
    template = loader.get_template('ajax/events/manage_options.html')
    t = template.render(RequestContext(request, locals()))
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def edit_option(request, option_id):

    # loads a form for editting an existing option

    option = MCQOption.objects.get(id=option_id)
    f = AddOptionForm(instance=option)
    template = loader.get_template('ajax/events/edit_option_form.html')
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
        template = loader.get_template('ajax/events/manage_options.html'
                )
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = \
            loader.get_template('ajax/events/edit_option_form.html')
        t = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#option_edit', 'innerHTML', t)
        return dajax.json()


@dajaxice_register
def add_edit_mobapp_tab(request, form=''):
    dajax = Dajax()
    event = request.user.get_profile().is_coord_of
    mob_app_tab = get_mob_app_tab(event)
    template = loader.get_template('ajax/events/add_edit_mobapptab.html'
                                   )
    if form:
        if mob_app_tab:
            f = MobAppWriteupForm(form, instance=mob_app_tab)
        else:
            f = MobAppWriteupForm(form)
        if f.is_valid():
            unsaved = f.save(commit=False)
            unsaved.event = event
            unsaved.save()
            dajax.alert('saved successfully!')
        else:
            dajax.alert('Error. Your write up could not be saved!')
    else:
        if mob_app_tab:
            f = MobAppWriteupForm(instance=mob_app_tab)
        else:
            f = MobAppWriteupForm()
    t = template.render(RequestContext(request, locals()))
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()

