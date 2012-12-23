from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.core.paginator import Paginator
import re,sys
import datetime
import json
from APIs.models import *
from HTMLParser import HTMLParser
import htmlentitydefs

#Html to plain text converter
#Code borrowed from @Soren\ Loveborg
class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()

#End of borrowed code

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
        if params == None or params.startswith('q='):
            start = None
            end = None
            page=None
            if params != None and params.startswith('q='):
                params = params[2:]
                options = params.split('&')
                try:
                    for i in range(0,len(options)):
                        if options[i].split('=')[0] == "start":
                            start = options[i].split('=')[1]
                        if options[i].split('=')[0] == "end":
                            end = options[i].split('=')[1]
                        if options[i].split('=')[0] == "page":
                            page = options[i].split('=')[1]

                except:
                    pass
            
            rendered['events'] = list()
            try:
                if page!=None:
                    events = Event.objects.all()
                    pagedEvents = Paginator(events,10)
                    events = pagedEvents.page(page).object_list
                    
                elif start == None and end == None:
                    events = Event.objects.all()
                elif start == None:
                    events = Event.objects.all()[:end]
                elif end == None:
                    events = Event.objects.all()[int(start)-1:]
                else:
                    events = Event.objects.all()[int(start)-1:end]
                for event in events:
                    rendered['events'].append({'title':event.title,'id':event.pk,'category':event.category})
            except:
                status = 500

        else:
            try:
                IntroTab =  MobAppTab.objects.get(event_id = params,title="Introduction")
                try:
                    FormatTab = MobAppTab.objects.get(event_id = params,title="Event Format")
                except:
                    FormatTab =  MobAppTab.objects.get(event_id = params,title="Introduction")
                try:
                    PrizeTab = MobAppTab.objects.get(event_id=params,title__icontains="Prize Money")
                    PrizeMoney  = html_to_text(PrizeTab.text)
                except:
                    PrizeMoney = "NA"

                updatesObject = Update.objects.filter(event = params,expired = False)
                updates = list()
                announcements = list()
                for update in updatesObject:
                    if update.category == "Update":
                        updates.append(html_to_text(update.description))
                    else:
                        announcements.append(html_to_text(update.description))
                
                Intro = html_to_text(IntroTab.text)
                Format = html_to_text(FormatTab.text)

                rendered = {'Introduction':Intro,'Event Format':Format,'Prize Money':PrizeMoney,'updates':updates,'announcements':announcements}
            except:
                status = 500
        
        rendered['status'] = status
        rendered = json.dumps(rendered) 
        
    return HttpResponse(rendered, mimetype='application/json')
 
def UpdateHandler(request,params=None):
    if(params!=None):
        try:
            updatesObject = Update.objects.filter(event = params,expired = False)
            updates = list()
            announcements = list()
            today_updates = list()
            today_announcements = list()
            today = datetime.now().date()
            for update in updatesObject:
                if update.category == "Update":
                    updates.append(html_to_text(update.description))
                    if update.date == today:
                        today_updates.append(html_to_text(update.description))
                else:
                    announcements.append(html_to_text(update.description))

                    if update.date == today:
                        today_announcements.append(html_to_text(update.description))

              
            rendered = {'updates':updates,'announcements':announcements,'Today_Update':today_updates,'Today_Announcements':today_announcements,'status':200}
        except:
            rendered = {'status':500}
        
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

       
