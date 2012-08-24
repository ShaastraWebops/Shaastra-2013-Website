from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from events.models import Event, EVENT_CATEGORIES, Tag
from django.template.defaultfilters import slugify

def home(request):
    event_set=[]
    for c in EVENT_CATEGORIES :
        event_category_set = Event.objects.filter(category=c[0])
        if event_category_set :
            event_set.append(event_category_set)
            
    #Code for search
    result_list=[]
    for t in Tag.objects.all():
        row=[]
        row.append(str(t.name))
        temp=[]
        for x in t.event_set.all():
            url = slugify(x) + '/tab/' + x.tab_set.all()[0].title
            temp.append([str(x),str(url)])
        row.append(temp)
        result_list.append(row)
    #End of search code
    
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect(settings.SITE_URL + 'admin/')
        elif request.user.get_profile().is_core:
            return HttpResponseRedirect(settings.SITE_URL + 'core/')
        elif request.user.get_profile().is_coord_of:
            return HttpResponseRedirect(settings.SITE_URL + 'coord/')
        else:
    	    return render_to_response('index.html',locals(),context_instance = RequestContext(request))
    else:
    	return render_to_response('index.html',locals(),context_instance = RequestContext(request))

def hospi(request):
    return render_to_response('hospi/hospi_home.html',locals(),context_instance = RequestContext(request))

def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404
