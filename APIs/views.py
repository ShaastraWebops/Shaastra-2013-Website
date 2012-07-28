from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
import re,sys
import json
from APIs.models import *

#Test function to test the POST APIs
def test(request):
    return render_to_response('test.html', locals(), context_instance=RequestContext(request))

def EventHandler(request,params=None):
    rendered = json.dumps({"status":"invalid code"})
    if request.method == "POST":
        rendered = json.dumps({"method":"POST","views":"event"})        
    else:
        rendered = dict()
        status = 200
        if params == None:
            rendered['events'] = list()
            try:
                events = Event.objects.all()
                for event in events:
                    rendered['events'].append({'title':event.title,'id':event.pk,'category':event.category})
            except:
                status = 500

        else:
            try:
                mobopsTab = MobAppTab.objects.get(event = params)
                updatesObject = Update.objects.filter(event = params,expired = False)
                updates = list()
                announcements = list()
                for update in updatesObject:
                    if update.category == "Update":
                        updates.append(update.description)
                    else:
                        announcements.append(update.description)

                rendered = {'text':mobopsTab.text,'updates':updates,'announcements':announcements}
            except:
                status = 500
        
        rendered['status'] = status
        rendered = json.dumps(rendered) 
        
    return HttpResponse(rendered, mimetype='application/json')
 
def UserHandler(request,params):
    rendered = json.dumps({"status":"invalid code"})
    if request.method == "POST":
        rendered = json.dumps({"method":"POST","views":"users"})        
    else:
        rendered = json.dumps({"method":"GET","views":"users"}) 
        
    return HttpResponse(rendered, mimetype='application/json')

def SessionsHandler(request,params):
    rendered = json.dumps({"status":"invalid code"})
    if request.method == "POST":
        rendered = json.dumps({"method":"POST","views":"sessions"})        
    else:
        rendered = json.dumps({"method":"GET","views":"sessions"}) 
        
    return HttpResponse(rendered, mimetype='application/json')

       
