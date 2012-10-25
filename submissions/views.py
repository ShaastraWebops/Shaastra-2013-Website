#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.models import User
from events.models import *
from submissions.models import *
from submissions.forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required


def get_answer(sub, q):
    try:
        return Answer_MCQ.objects.get(question=q, submission=sub)
    except:
        return None


def get_answer_text(sub, q):
    try:
        return Answer_Text.objects.get(question=q, submission=sub)
    except:
        return None


def get_elem(index, pag_list, n):
    if index + n < 0:
        return None
    try:
        return pag_list[index + n]
    except:
        return None


def registrable(eve_id):
    event = Event.objects.get(id=eve_id)
    if event.begin_registration and event.registrable_online:
        return True
    return False


# Create your views here.

@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def submissions(request):
    subs = \
        request.user.get_profile().is_coord_of.basesubmission_set.all()
    return render_to_response('ajax/submissions/all_submissions.html',
                              locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def all_submissions(request):
    if request.method == 'GET':
        submissions = \
            request.user.get_profile().individualsubmission_set.all()
        return render_to_response('submissions/submission_list.html',
                                  locals(),
                                  context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def event_submission(request, **kw):
    if request.method == 'GET':
        if not registrable(kw['event_id']):
            return HttpResponse('Registrations are closed')
        event = Event.objects.get(id=kw['event_id'])
        if not event.has_questionnaire:
            pro = request.user.get_profile()
            if event in pro.registered_events.all():
                return HttpResponse('You have already registered for this event.'
                                    )
            pro.registered_events.add(event)
            pro.save()
            return HttpResponse('Thank you for registering.')
        mcqs = event.objectivequestion_set.all()
        subjectives = event.subjectivequestion_set.all()
        return render_to_response('submissions/submission.html',
                                  locals(),
                                  context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def save_edit_mcq(
    request,
    eve_id,
    q_id,
    is_mcq=True,
    ):
    if not registrable(eve_id):
        return HttpResponse('Registrations are closed')
    sub = IndividualSubmission.objects.get_or_create(event_id=eve_id,
            participant=request.user.get_profile())[0]
    q = ObjectiveQuestion.objects.get(id=q_id)
    ans = get_answer(sub, q)
    f = Answer_MCQ_Form(queryset=q.mcqoption_set.all(),
                        initial={'choice': ans})
    q = \
        (ObjectiveQuestion.objects.get(id=q_id) if is_mcq else SubjectiveQuestion.objects.get(id=q_id))
    pag_list = []
    objects1 = \
        ObjectiveQuestion.objects.filter(event__id=eve_id).only('id',
            'q_number')
    objects2 = \
        SubjectiveQuestion.objects.filter(event__id=eve_id).only('id',
            'q_number')
    for obj in objects1:
        pag_list.append([obj.id, obj.q_number, True])
    for obj in objects2:
        pag_list.append([obj.id, obj.q_number, False])
    index = pag_list.index([int(q_id), q.q_number, is_mcq])
    prev_elem = get_elem(index, pag_list, -1)
    next_elem = get_elem(index, pag_list, +1)
    return render_to_response('ajax/submissions/mcq_form.html',
                              locals(),
                              context_instance=RequestContext(request))


@login_required(login_url=settings.SITE_URL + 'user/ajax_login/')
def save_edit_subjective(
    request,
    eve_id,
    q_id,
    is_mcq=False,
    ):
    if not registrable(eve_id):
        return HttpResponse('Registrations are closed')
    sub = IndividualSubmission.objects.get_or_create(event_id=eve_id,
            participant=request.user.get_profile())[0]
    q = SubjectiveQuestion.objects.get(id=q_id)
    ans = get_answer_text(sub, q)
    f = Answer_Text_Form(instance=ans)
    q = \
        (ObjectiveQuestion.objects.get(id=q_id) if is_mcq else SubjectiveQuestion.objects.get(id=q_id))
    pag_list = []
    objects1 = \
        ObjectiveQuestion.objects.filter(event__id=eve_id).only('id',
            'q_number')
    objects2 = \
        SubjectiveQuestion.objects.filter(event__id=eve_id).only('id',
            'q_number')
    for obj in objects1:
        pag_list.append([obj.id, obj.q_number, True])
    for obj in objects2:
        pag_list.append([obj.id, obj.q_number, False])
    index = pag_list.index([int(q_id), q.q_number, is_mcq])
    prev_elem = get_elem(index, pag_list, -1)
    next_elem = get_elem(index, pag_list, +1)
    return render_to_response('ajax/submissions/textq_form.html',
                              locals(),
                              context_instance=RequestContext(request))

#TODO:Change upload to path while pushing
@login_required(login_url=settings.LOGIN_URL)
def submittdp(request,event_id):
    msg = "IMPORTANT:Please upload file in PDF format only."
    usr = request.user
    profile = usr.get_profile()
    evt = Event.objects.get( id = event_id )
    registered = 0
    form = TDPSubmissionForm() 
    #Check if user is registered for event
    if evt.has_tdp:
        if evt.team_event:
            teams = Team.objects.filter( event = evt )
            for t in teams:
                members = t.members.objects.all()
                for m in members:
                    if usr is m:
                        registered = 1
                        current_team = t
        else:
            try:
                participant = EventSingularRegistration.objects.get(event = evt, user = usr)
                registered = 1  
            except:
                registered = 0 
        #If registered check if submission already made.  
        if registered == 1:
            try:
                submission = TDPSubmissions.objects.get( team = current_team, basesub__event = evt)  
            except:
                try:
                    submission = TDPSubmissions.objects.get( participant = usr, basesub__event = evt)  
                except:            
                    if request.method == 'POST': 
                        form = TDPSubmissionForm(request.POST, request.FILES) 
                        if form.is_valid():
                            basesub = BaseSubmission(event = evt, submitted = True)
                            basesub.save()
                            #Create a BaseSub first and connect TDP to it.
                            submission = form.save(commit=False)
                            submission.basesub = basesub
                            try: 
                                if current_team:
                                    submission.team = team
                                    submission.save()
                                    msg = "Your TDP has been submitted successfully. Thank You."
                            except:
                                submission.participant = usr
                                submission.save()
                                msg = "Your TDP has been submitted successfully. Thank You."
        return render_to_response('ajax/submissions/submittdp.html',locals(),context_instance=RequestContext(request))
    return render_to_response('ajax/submissions/submittdp.html',locals(),context_instance=RequestContext(request))

@login_required(login_url=settings.LOGIN_URL)
def ViewTdpSubmissions(request):
    try:    
        evt = request.user.get_profile().is_coord_of
        subs = TDPSubmissions.objects.filter(basesub__event = evt)
    except:
        raise Http404()
    return render_to_response('ajax/submissions/all_tdp_submissions.html',
                          locals(),
                          context_instance=RequestContext(request))


