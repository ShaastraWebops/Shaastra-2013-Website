from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.models import User
from events.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def submissions(request):
    subs = request.user.get_profile().is_coord_of.basesubmission_set.all()
    return render_to_response('ajax/submissions/all_submissions.html', locals(), context_instance = RequestContext(request))

@login_required
def all_submissions(request):
    if request.method == 'GET':
        submissions = request.user.get_profile().individualsubmission_set.all()
        return render_to_response('submissions/submission_list.html', locals(), context_instance = RequestContext(request))
        
@login_required
def event_submission(request, **kw):
    if request.method == 'GET':
        event = Event.objects.get(id = kw['event_id'])
        mcqs = event.objectivequestion_set.all()
        subjectives = event.subjectivequestion_set.all()
        return render_to_response('submissions/submission.html', locals(), context_instance = RequestContext(request))
