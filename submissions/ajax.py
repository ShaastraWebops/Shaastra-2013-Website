#!/usr/bin/python
# -*- coding: utf-8 -*-
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
        return Answer_MCQ.objects.get(question=q, submission=sub)
    except:
        return None


def get_answer_text(sub, q):
    try:
        return Answer_Text.objects.get(question=q, submission=sub)
    except:
        return None


@dajaxice_register
def save_edit_mcq(
    request,
    eve_id,
    q_id,
    form,
    ):
    sub = IndividualSubmission.objects.get_or_create(event_id=eve_id,
            participant=request.user.get_profile())[0]
    dajax = Dajax()
    q = ObjectiveQuestion.objects.get(id=q_id)
    choice = q.mcqoption_set.get(id=int(form['choice']))
    ans = Answer_MCQ.objects.get_or_create(question_id=q_id,
            submission=sub)[0]
    ans.choice = choice
    ans.save()
    dajax.alert('save sucessful')
    f = Answer_MCQ_Form(queryset=q.mcqoption_set.all())
    return dajax.json()


@dajaxice_register
def save_edit_subjective(
    request,
    eve_id,
    q_id,
    form,
    ):
    sub = IndividualSubmission.objects.get_or_create(event_id=eve_id,
            participant=request.user.get_profile())[0]
    dajax = Dajax()
    q = SubjectiveQuestion.objects.get(id=q_id)
    ans = get_answer_text(sub, q)
    f = Answer_Text_Form(form, instance=ans)
    if f.is_valid():
        if not ans:
            unsaved_ans = f.save(commit=False)
            unsaved_ans.question = q
            unsaved_ans.submission = sub
            unsaved_ans.save()
        else:
            f.save()
        dajax.alert('save successful')
    else:
        dajax.alert('Your answer could not be saved')
    return dajax.json()


# coord related ajax views start from here
@dajaxice_register
def all_submissions(request):
    return submission_list(request)


def submission(request, sub_id, mark_read=False):
    dajax = Dajax()
    sub = BaseSubmission.objects.get(id=sub_id)
    if mark_read:
        sub.sub_read = True
        sub.save()
    mcqs = Answer_MCQ.objects.filter(submission=sub)
    textqs = Answer_Text.objects.filter(submission=sub)
    template = \
        loader.get_template('ajax/submissions/view_submission.html')
    t = template.render(RequestContext(request, locals()))
    dajax.assign('.bbq-item', 'innerHTML', t)
    return dajax.json()


@dajaxice_register
def view_submission(request, sub_id):
    return submission(request, sub_id, mark_read=True)


@dajaxice_register
def edit_sub(
    request,
    sub_id,
    attr,
    assign,
    ):
    kw = {'false': False, 'true': True}
    sub = BaseSubmission.objects.get(id=sub_id)
    setattr(sub, attr, kw[assign])
    sub.save()
    return submission(request, sub_id)


@dajaxice_register
def save_score(request, form, sub_id):
    print 'here'
    sub = BaseSubmission.objects.get(id=sub_id)
    sub.score = form['score']
    sub.save()
    return submission(request, sub_id)

