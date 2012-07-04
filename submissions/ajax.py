from dajax.core import Dajax
from django.utils import simplejson
from django.template import loader, Context, RequestContext, Template
from dajaxice.decorators import dajaxice_register
from events.models import *
from users.models import *
from submissions.models import *
from django.core.paginator import Paginator

def get_answer(sub, q):
    try:
        return Answer_MCQ.objects.get(question = q, submission = sub)
    except: 
        return None
        
def get_answer_text(sub, q):
    try:
        return Answer_Text.objects.get(question = q, submission = sub)
    except: 
        return None

def get_elem(index, pag_list, n):
    if index+n<0:
        return None
    try:
        return pag_list[index+n]
    except:
        return None
        
@dajaxice_register
def save_edit_mcq(request, eve_id, q_id, form = ''):
    sub = IndividualSubmission.objects.get_or_create(event_id = eve_id, participant = request.user.get_profile())[0]
    dajax = Dajax()
    q = ObjectiveQuestion.objects.get(id = q_id)
    jav_func = None
    if form:
        choice = q.mcqoption_set.get(id = int(form['choice']))
        ans = Answer_MCQ.objects.get_or_create(question_id = q_id, submission = sub)[0]
        ans.choice = choice
        ans.save()
        dajax.alert('save sucessful')
        f = Answer_MCQ_Form(queryset = q.mcqoption_set.all())
        jav_func = """var elem = getRadioByValue(%s);
        setChecked(elem);""" % choice.id
    else:
        ans = get_answer(sub, q)
        f = Answer_MCQ_Form(queryset = q.mcqoption_set.all())
        if ans:
            jav_func = """var id = getRadioByValue(%s);
            setChecked(id);""" % ans.choice.id
    template = loader.get_template('ajax/submissions/mcq_form.html')
    t = template.render(RequestContext(request,locals())) 
    dajax.assign('#q_detail', 'innerHTML', t)
    dajax.script(jav_func)
    dajax.script('pagination(%s,%s,true);' % (eve_id, q_id))
    return dajax.json()
        
@dajaxice_register
def save_edit_subjective(request, eve_id, q_id, form = ''):
    sub = IndividualSubmission.objects.get_or_create(event_id = eve_id, participant = request.user.get_profile())[0]
    dajax = Dajax()
    q = SubjectiveQuestion.objects.get(id = q_id)
    ans = get_answer_text(sub, q)
    if form:
        f = Answer_Text_Form(form, instance = ans)
        if f.is_valid():
            if not ans:
                unsaved_ans = f.save(commit = False)
                unsaved_ans.question = q
                unsaved_ans.submission = sub
                unsaved_ans.save()
            else:
                f.save()
            dajax.alert('save successful')
    else:
        f = Answer_Text_Form(instance = ans)
    template = loader.get_template('ajax/submissions/textq_form.html')
    t = template.render(RequestContext(request, locals())) 
    dajax.assign('#q_detail', 'innerHTML', t)
    dajax.script('pagination(%s,%s,false);' % (eve_id, q_id))
    return dajax.json()
    
@dajaxice_register    
def pagination(request, eve_id, q_id, is_mcq):
    dajax = Dajax()
    q = ObjectiveQuestion.objects.get(id = q_id) if is_mcq else SubjectiveQuestion.objects.get(id = q_id)
    pag_list = []
    objects1 = ObjectiveQuestion.objects.filter(event__id = eve_id).only('id', 'q_number')
    objects2 = SubjectiveQuestion.objects.filter(event__id = eve_id).only('id', 'q_number')
    for obj in objects1:
        pag_list.append([obj.id, obj.q_number, True])
    for obj in objects2:        
        pag_list.append([obj.id, obj.q_number, False])
    index = pag_list.index([int(q_id), q.q_number, is_mcq])
    prev_elem = get_elem(index, pag_list, -1)
    next_elem = get_elem(index, pag_list, +1)
    template = loader.get_template('ajax/submissions/paginate.html')
    t = template.render(RequestContext(request, locals()))
    dajax.assign('#pagination', 'innerHTML', t)
    return dajax.json()

# coord related ajax views start from here

def submission_list(request):
    dajax = Dajax()
    subs = request.user.get_profile().is_coord_of.basesubmission_set.all()
    template = loader.get_template('ajax/submissions/all_submissions.html')
    t = template.render(RequestContext(request,locals())) 
    dajax.assign('#detail', 'innerHTML', t)
    dajax.script("$('#submissions_list').dataTable();")
    return dajax.json()
    
@dajaxice_register
def all_submissions(request):
    return submission_list(request)

def submission(request, sub_id, mark_read = False):    
    dajax = Dajax()
    sub = BaseSubmission.objects.get(id = sub_id)
    if mark_read: 
        sub.sub_read = True
        sub.save()
    mcqs = Answer_MCQ.objects.filter(submission = sub)
    textqs = Answer_Text.objects.filter(submission = sub)
    template = loader.get_template('ajax/submissions/view_submission.html')
    t = template.render(RequestContext(request,locals()))
    dajax.assign('#detail', 'innerHTML', t)
    return dajax.json()
    
@dajaxice_register
def view_submission(request, sub_id):
    return submission(request, sub_id, mark_read = True)

@dajaxice_register
def edit_sub(request, sub_id, attr, assign):
    kw = {'false':False, 'true':True}
    sub = BaseSubmission.objects.get(id = sub_id)
    setattr(sub, attr, kw[assign])
    sub.save()
    return submission(request, sub_id)
    
@dajaxice_register
def send_checklist(request, form):
    dajax = Dajax()
    assign = True
    if form['action'] == 'sub_read': assign = False
    if form['action'] == 'read': form['action'] = 'sub_read'
    sub_ids = [form['sub_checklist']] if len(form['sub_checklist'])==1 else form['sub_checklist']
    for sub_id in sub_ids:
        sub = BaseSubmission.objects.get(id = sub_id)
        setattr(sub, form['action'], assign)
        sub.save()
    return submission_list(request)

@dajaxice_register    
def save_score(request, form, sub_id):
    print 'here'
    sub = BaseSubmission.objects.get(id = sub_id)
    sub.score = form['score']
    sub.save()
    return submission(request, sub_id)
    
