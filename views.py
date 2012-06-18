from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response

def home(request):
    if request.user.is_authenticated() and request.user.is_superuser :
        return HttpResponseRedirect('/admin')
    else:
    	return render_to_response('home.html',locals(),context_instance = RequestContext(request))
	
def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404
