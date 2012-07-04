from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.conf import settings

@login_required(login_url=settings.SITE_URL + 'user/login/')
def home(request):
    """
        This is the home page view of the superuser
    """
#    a=request.META['SCRIPT_NAME']
#    assert False
    if request.user.is_superuser is False :
        return HttpResponseRedirect(settings.SITE_URL)
    return render_to_response('admin/home.html', locals(), context_instance = RequestContext(request))