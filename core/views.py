from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.conf import settings

@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    """
        This is the home page view of the core
    """
    if request.user.get_profile().is_core is False :
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('core/home.html', locals(), context_instance = RequestContext(request))



