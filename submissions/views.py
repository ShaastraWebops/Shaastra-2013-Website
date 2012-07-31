from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.models import User
from events.models import *
from submissions.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required


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
        
def registrable(eve_id):
    event = Event.objects.get(id = eve_id)
    if event.begin_registration and event.registrable_online: return True
    return False

# Create your views here.
@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def submissions(request):
    subs = request.user.get_profile().is_coord_of.basesubmission_set.all()
    return render_to_response('ajax/submissions/all_submissions.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def all_submissions(request):
    if request.method == 'GET':
        submissions = request.user.get_profile().individualsubmission_set.all()
        return render_to_response('submissions/submission_list.html', locals(), context_instance = RequestContext(request))
        
@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def event_submission(request, **kw):
    if request.method == 'GET':
        if not registrable(kw['event_id']): return HttpResponse('Registrations are closed')
        event = Event.objects.get(id = kw['event_id'])
        if not event.has_questionnaire:
            pro = request.user.get_profile()
            if event in pro.registered_events.all(): return HttpResponse('You have already registered for this event.')
            pro.registered_events.add(event)
            pro.save()
            return HttpResponse('Thank you for registering.')
        mcqs = event.objectivequestion_set.all()
        subjectives = event.subjectivequestion_set.all()
        return render_to_response('submissions/submission.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def save_edit_mcq(request, eve_id, q_id, is_mcq = True):
    if not registrable(eve_id): return HttpResponse('Registrations are closed')
    sub = IndividualSubmission.objects.get_or_create(event_id = eve_id, participant = request.user.get_profile())[0]
    q = ObjectiveQuestion.objects.get(id = q_id)
    ans = get_answer(sub, q)
    f = Answer_MCQ_Form(queryset = q.mcqoption_set.all(), initial = {'choice':ans})
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
    return render_to_response('ajax/submissions/mcq_form.html', locals(), context_instance = RequestContext(request))

@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')        
def save_edit_subjective(request, eve_id, q_id, is_mcq = False):
    if not registrable(eve_id): return HttpResponse('Registrations are closed')
    sub = IndividualSubmission.objects.get_or_create(event_id = eve_id, participant = request.user.get_profile())[0]
    q = SubjectiveQuestion.objects.get(id = q_id)
    ans = get_answer_text(sub, q)
    f = Answer_Text_Form(instance = ans)
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
    return render_to_response('ajax/submissions/textq_form.html', locals(), context_instance = RequestContext(request))
