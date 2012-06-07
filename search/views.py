import shlex
#import redis
from search.models import * #Needs to be updated with actual class Event
from django.http import *
from django.shortcuts import *
from django.db.models import Q

#event_tag=redis.Redis("localhost")

def home(request):
    event=Event.objects.all()
    return render_to_response("home.html",locals())
    
def addevent(request): #This function is present for testing search functionality only. Functionality to check if event and auto-added tag(Event name itself) is unique needs to be added.
    if request.method == 'POST':
        event=Event(name=request.POST['event_name'])
        event.save()
        temp=Tag(tag=request.POST['event_name'].lower())
        temp.save()
        event.tag.add(temp)
        return HttpResponseRedirect("../")
    return render_to_response("addevent.html", locals(), context_instance=RequestContext(request))

"""
def addredistag(derived_tag, event_name, main_tag):
    event_tag.sadd(derived_tag, event_name)
    event_tag.sadd("tags", derived_tag)
    event_tag.sadd("root:%s" % derived_tag, main_tag)
  
def delredistag(derived_tag, event_name, main_tag):
    flag=0
    if len(event_tag.smembers("root:%s" % derived_tag))==1 and len(event_tag.smembers(derived_tag))==1:
        event_tag.delete(derived_tag)
        event_tag.delete("root:%s" % derived_tag)
        event_tag.srem("tags", derived_tag)
    elif len(event_tag.smembers("root:%s" % derived_tag))==1 and len(event_tag.smembers(derived_tag))!=1:
        event_tag.srem(derived_tag, event_name)
    elif len(event_tag.smembers("root:%s" % derived_tag))!=1 and len(event_tag.smembers(derived_tag))==1:
        event_tag.srem("root:%s" % derived_tag, main_tag)
    else:
        for x in event_tag.smembers("root:%s" % derived_tag):
            if x!=main_tag:
                if event_name in event_tag.smembers(x):
                    flag=1
                    break
        if flag==0:
            event_tag.srem(derived_tag, event_name)
"""
def tags_alphabetical(tags):
    tag_names=[]
    temp_tags=[]
    for x in tags:
        tag_names.append(x.tag)
    tag_names.sort()
    for x in tag_names:
        for y in tags:
            if y.tag==x:
                temp_tags.append(y)
    return temp_tags

def event(request, eventid):
    existing = request.GET.get('existing', None)
    add = request.GET.get('add', None)
    tag_edited = request.GET.get('tag_edited', None)
    event=Event.objects.get(pk=eventid)
    tag_list=Tag.objects.filter(event=event)
    all_tags=Tag.objects.filter(~Q(event=event))
    
    tag_list=tags_alphabetical(tag_list)
    all_tags=tags_alphabetical(all_tags)
        
    not_added=[]
    flag=0
    
    if request.method=='POST':
        if 'add' in request.POST:
            tags=request.POST['tags']
            tags=tags.lower()
            tags=[x.strip() for x in tags.split(',')]
            for t in tags:
                if len(t)>=3:
                    try:
                        x=Tag.objects.get(tag=t)
                    except Tag.DoesNotExist:
                        temp=Tag(tag=t)
                        temp.save()
                        event.tag.add(temp)
                        i=len(t)
                        event_name=str(event)
                        #while i>=3:
                        #    addredistag(t[0:i], event_name, t)
                        #    i-=1
                        #event_tag.save()
                    else:
                        if not event in x.event_set.all():
                            event.tag.add(x)
                            i=len(t)
                            event_name=str(event)
                            #while i>=3:
                            #    addredistag(t[0:i], event_name, t)
                            #    i-=1
                            #event_tag.save()
                        else:
                            flag=1
                else:
                    not_added.append(t)            
            if not not_added:
                tags_added=True
            else:
                tags_notadded=True   
                
        if 'select' in request.POST:
            tag_existing=request.POST.getlist('tag_existing')
            for i in tag_existing:
                t=Tag.objects.get(pk=i)
                t_tag=str(t)
                event.tag.add(t)
                length=len(t_tag)
                event_name=str(event)
                #while length>=3:
                #    addredistag(t_tag[0:length], event_name, t_tag)
                #    length-=1
                #event_tag.save()
            tags_added=True
            
        if 'delete' in request.POST:
            tag_delete=request.POST.getlist('tag_delete')
            for i in tag_delete:
                t=Tag.objects.get(pk=i)
                t_tag=str(t)
                event.tag.remove(t)
                flag=0
                length=len(t_tag)
                event_name=str(event)
                #while length>=3:
                #    delredistag(t_tag[0:length], event_name, t_tag)
                #    length-=1
                #event_tag.save()
                if not t.event_set.all():
                    t.delete()
                tags_deleted=True
    return render_to_response("event.html", locals(), context_instance=RequestContext(request))

def edittag(request, eventid, tagid):
    tag=Tag.objects.get(pk=tagid)
    event=Event.objects.get(pk=eventid)
    edited=0
    if request.method=='POST':
        t=request.POST['tag_edit']
        t=t.lower()
        if ',' in t:
            comma=1
            tag=Tag(tag=t)
            return render_to_response("edittag.html", locals(), context_instance=RequestContext(request))
        else:
            if len(t)>=3:
                try:
                    x=Tag.objects.get(tag=t)
                except Tag.DoesNotExist:
                    temp=Tag(tag=t)
                    temp.save()
                    event.tag.add(temp)
                    t=str(t)
                    i=len(t)
                    event_name=str(event)
                    
                    #while i>=3:
                    #    addredistag(t[0:i], event_name, t)
                    #    i-=1
                    #event_tag.save()
                    edited=1
                else:
                    if not event in x.event_set.all():
                        event.tag.add(x)
                        i=len(t)
                        event_name=str(event)
                        #while i>=3:
                        #    addredistag(t[0:i], event_name, t)
                        #    i-=1
                        #event_tag.save()
                        edited=1
                    else:
                        already_present=1
                        tag=Tag(tag=t)
                        return render_to_response("edittag.html", locals(), context_instance=RequestContext(request))
            else:
                not_long=1
                tag=Tag(tag=t)
                return render_to_response("edittag.html", locals(), context_instance=RequestContext(request))
        tag=Tag.objects.get(pk=tagid)
        event.tag.remove(tag)
        t=str(tag)
        flag=0
        length=len(t)
        event_name=str(event)
        #while length>=3:
        #    delredistag(t[0:length], event_name, t)
        #    length-=1
        #event_tag.save()
        if not tag.event_set.all():
            tag.delete()
        tag=Tag(tag=t)
        if edited:
            html='../event/%s/?tag_edited=True' % eventid
            return HttpResponseRedirect(html)
    return render_to_response("edittag.html", locals(), context_instance=RequestContext(request))

def main(request):
    return render_to_response("main.html", locals())

def main2(request):
    result_list=[]
    for t in Tag.objects.all():
        row=[]
        row.append(str(t.tag))
        temp=[]
        for x in t.event_set.all():
            temp.append([str(x),str(x.id)])
        row.append(temp)
        result_list.append(row)
    return render_to_response("main2.html", locals(), context_instance=RequestContext(request))

def search(request):
    query_string = request.GET.get('q', None)
    query_string = query_string.lower()
    results=[]
    query_list=[]
    if query_string==None:
        return render_to_response("search.html", locals())  
    
    if " " in query_string:
        query_list=shlex.split(query_string) #shlex splits 'Hello "how are" you' as ['Hello','how are', 'you']
    query_list.append(query_string) #to check for an exact match as well.
    
    #for query in query_list:
    #    if event_tag.sismember("tags", query): #check if such a tag exists
    #        results+=list(event_tag.smembers(query))
    #results.sort()
    result_list=[]
    for r in results:
        result_list.append(Event.objects.get(name=r))  
    return render_to_response("search.html", locals())

def eventdetails(request, eventid):
    r=Event.objects.get(pk=eventid)
    return render_to_response("eventdetails.html", locals())
