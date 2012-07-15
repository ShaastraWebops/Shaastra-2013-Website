import random
from dajax.core import Dajax
from django.utils import simplejson
from django.template import loader, Context, RequestContext, Template
from events.models import *
from events.forms import *
from dajaxice.decorators import dajaxice_register

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
def updateTabs(request):
    """
    This function updates the tabs div
    """
    dajax = Dajax()
    event = request.user.get_profile().is_coord_of
    tabs=get_tabs(event)
    dajax.assign("#tabs", 'innerHTML', '')
    for tab in tabs:
        dajax.append("#tabs",'innerHTML',"<a href="+'#customtabs/'+str(tab.id)+" name ="+tab.title+" id ="+ str(tab.id)+" >"+tab.title+"</a> ")
    dajax.script("window.location.hash='';")
    return dajax.json()
        
@dajaxice_register
def delete_tab(request, tab_id=0):
    # deletes the tab. shows a delete successful message.
    dajax = Dajax()
    if tab_id:
        tab = Tab.objects.get(id = tab_id)
        title = tab.title
        tab.delete()
        dajax.alert(title+' deleted sucessfully!')
        dajax.script("Dajaxice.events.updateTabs(Dajax.process);");
    else:
        dajax.alert('error '+ tab_id)
    return dajax.json()
        
@dajaxice_register
def save_tab(request, data, tab_id=0):
    # validates the tab details that were submitted while adding a new tab
    dajax = Dajax()
    if tab_id:
        tab = Tab.objects.get(id = tab_id)
        form = TabAddForm(data, instance = tab)
    else:
        form = TabAddForm(data)
    if form.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_tab = form.save(commit = False)
        unsaved_tab.event = event
        unsaved_tab.save()
        tab = unsaved_tab
        if not tab_id:
            dajax.append('#tabs','innerHTML',"<a href="+'#customtabs/'+str(tab.id)+" name ="+str(tab.title)+" id ="+str(tab.id)+" > "+str(tab.title)+"  </a>")
        dajax.script("window.location.hash='"+'customtabs/'+str(tab.id)+"';")
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/tab_form.html')
        html = template.render(RequestContext(request,locals()))
        dajax.assign('.bbq-item', 'innerHTML', html)
        dajax.script("niced = new nicEditor().panelInstance('niced_text');")
        return dajax.json()
    
@dajaxice_register
def delete_file(request, tab_id, file_id):
    # deletes the selected file
    form = TabFile.objects.get(id = file_id)
    form.delete()
    tab = Tab.objects.get(id = tab_id)
    file_list = get_files(tab)
    template = loader.get_template('ajax/events/tab_detail.html')
    html = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item','innerHTML', html)
    return dajax.json()
        
@dajaxice_register
def rename_file_done(request, form, file_id):
    # renames a file
    f = TabFile.objects.get(id = file_id)
    if form['display_name']:
        f.title = form['display_name']
        f.save()
    tab = f.tab
    file_list = get_files(tab)
    template = loader.get_template('ajax/events/tab_detail.html')
    html = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('.bbq-item','innerHTML', html)
    return dajax.json()
    
@dajaxice_register
def save_subjective(request, data, ques_id=0):
    # validates and saves a subjective question
    dajax = Dajax()
    if ques_id :
        ques = SubjectiveQuestion.objects.get(id = ques_id)
        form = AddSubjectiveQuestionForm(data, instance = ques)
    else:
        form = AddSubjectiveQuestionForm(data)
    if form.is_valid():
        event = request.user.get_profile().is_coord_of
        unsaved_ques = form.save(commit = False)
        unsaved_ques.event = event
        unsaved_ques.save()
        dajax.script("window.location.hash='questions'")
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/subj_form.html')
        html = template.render(RequestContext(request,locals()))
        dajax.assign('.bbq-item', 'innerHTML', html)
        return dajax.json()

@dajaxice_register        
def delete_subjective(request, ques_id):
    # deletes the selected question
    ques = SubjectiveQuestion.objects.get(id = ques_id)
    ques.delete()
    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/events/question_tab.html')
    html = template.render(RequestContext(request,locals())) 
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()

def saving_mcq(data, mcq):
    data.pop('csrfmiddlewaretoken')
    mcq.title = data.pop('title')
    mcq.q_number = data.pop('q_no')
    print data
    mcq.save()
    try:
        options = mcq.mcqoption_set.all()
    except:
        options = []
    keys = data.keys()
    keys.sort()
    print keys
    for opt_id in keys:
        if not data[opt_id]: continue
        if not opt_id.startswith('o'):
            print 'not'
            print opt_id[:-1]
            mcqoption = MCQOption(id = opt_id[:-1])
            print 'h'
        else:
            print 'else'
            mcqoption = MCQOption()
            print 'here'
        mcqoption.option = opt_id[-1]
        mcqoption.text = data[opt_id]
        mcqoption.question = mcq
        mcqoption.save()
    
@dajaxice_register
def save_mcq(request, data, ques_id):
    mcq = ObjectiveQuestion.objects.get(id = ques_id) if ques_id else ObjectiveQuestion(event = request.user.get_profile().is_coord_of)
    saving_mcq(data, mcq)
    ques_id = mcq.id
    options = mcq.mcqoption_set.all()
    template = loader.get_template('ajax/events/mcq_form.html')
    form = MCQForm(mcq, options)
    html = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.script('alert("question saved succesfully");')
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()
    
@dajaxice_register        
def delete_mcq(request, ques_id):
    # deletes the selected mcq
    ques = ObjectiveQuestion.objects.get(id = ques_id)
    ques.delete()
    event = request.user.get_profile().is_coord_of
    text_questions = event.subjectivequestion_set.all()
    mcqs = event.objectivequestion_set.all()
    template = loader.get_template('ajax/events/question_tab.html')
    t = template.render(RequestContext(request,locals())) 
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', t)
    return dajax.json()
    
@dajaxice_register        
def manage_options(request, ques_id):
    # all existing options displayed with features of editing/deleting them and adding new ones
    ques = ObjectiveQuestion.objects.get(id = ques_id)
    options = ques.mcqoption_set.all()
    template = loader.get_template('ajax/events/manage_options.html')
    html = template.render(RequestContext(request,locals())) 
    dajax = Dajax()
    dajax.assign('.bbq-item', 'innerHTML', html)
    return dajax.json()
    
@dajaxice_register
def add_option(request, ques_id):
    # displays a form for adding an option
    ques = ObjectiveQuestion.objects.get(id = ques_id)
    f = AddOptionForm()
    template = loader.get_template('ajax/events/add_option_form.html')
    t = template.render(RequestContext(request,locals())) 
    dajax = Dajax()
    dajax.assign('#option_edit', 'innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def save_option(request, form, ques_id):
    # validates and saves an option
    f = AddOptionForm(form)
    ques = ObjectiveQuestion.objects.get(id = ques_id)
    if f.is_valid():
        unsaved_option = f.save(commit = False)
        unsaved_option.question = ques
        unsaved_option.save()
        options = ques.mcqoption_set.all()
        template = loader.get_template('ajax/events/manage_options.html')
        t = template.render(RequestContext(request,locals())) 
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/add_option_form.html')
        t = template.render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#option_edit', 'innerHTML', t)
        return dajax.json()
        
@dajaxice_register
def delete_option(request, option_id):
    # deletes an option
    option = MCQOption.objects.get(id = option_id)
    ques = option.question
    option.delete()
    options = ques.mcqoption_set.all()
    template = loader.get_template('ajax/events/manage_options.html')
    t = template.render(RequestContext(request,locals())) 
    dajax = Dajax()
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def edit_option(request, option_id):
    # loads a form for editting an existing option
    option = MCQOption.objects.get(id = option_id)
    f = AddOptionForm(instance = option)
    template = loader.get_template('ajax/events/edit_option_form.html')
    t = template.render(RequestContext(request,locals()))
    dajax = Dajax()
    dajax.assign('#option_edit','innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def save_editted_option(request, form, option_id):
    # validates and saves editted option
    option = MCQOption.objects.get(id = option_id)
    ques = option.question
    f = AddOptionForm(form, instance = option)
    if f.is_valid():
        f.save()
        options = ques.mcqoption_set.all()
        template = loader.get_template('ajax/events/manage_options.html')
        t = template.render(RequestContext(request,locals())) 
        dajax = Dajax()
        dajax.assign('#detail', 'innerHTML', t)
        return dajax.json()
    else:
        template = loader.get_template('ajax/events/edit_option_form.html')
        t = template.render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#option_edit', 'innerHTML', t)
        return dajax.json()

@dajaxice_register
def add_edit_mobapp_tab(request, form = ''):
    dajax = Dajax()
    event = request.user.get_profile().is_coord_of
    mob_app_tab = get_mob_app_tab(event)
    template = loader.get_template('ajax/events/add_edit_mobapptab.html')
    if mob_app_tab:
        f = MobAppWriteupForm(form, instance = mob_app_tab)
    else:
        f = MobAppWriteupForm(form)
    if f.is_valid():
        unsaved = f.save(commit = False)
        unsaved.event = event
        unsaved.save()
        dajax.alert('saved successfully!')
        dajax.script("window.location.hash='';")
    else:
        dajax.alert('Error. Your write up could not be saved!')
        t = template.render(RequestContext(request,locals())) 
        dajax.assign('.bbq-item', 'innerHTML', t)
    return dajax.json()
    
