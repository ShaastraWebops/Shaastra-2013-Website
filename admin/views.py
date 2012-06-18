from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext

@login_required(login_url='/user/login')
def home(request):
    """
        This is the home page view of the superuser
    """
    if request.user.is_superuser is False :
        return HttpResponseRedirect('/')
    return render_to_response('admin/home.html', locals(), context_instance = RequestContext(request))



