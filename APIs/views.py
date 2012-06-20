from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
import re,sys
import json

#Test function to test the POST APIs
def test(request):
    return render_to_response('test.html', locals(), context_instance=RequestContext(request))

def EventHandler(request,params):
    rendered = json.dumps({"status":"invalid code"})
    if request.method == "POST":
        rendered = json.dumps({"method":"POST","views":"event"})        
    else:
        rendered = json.dumps({"method":"GET","views":"event"}) 
        
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

       
