import shlex
import redis
from search.models import Event #Needs to be updated with actual class Event

def search(query_string):
    """
    event -> set([list of tags])
    """
    event_tag=redis.Redis("localhost")
    
    event_list=[]
    results=[]
    
    if ' ' in query_string:
        query_list=shlex.split(query_string) #shlex splits 'Hello "how are" you' as ['Hello','how are', 'you']
    query_list.append(query_string) #to check for an exact match as well.
    
    for query in query_list:
        if event_tag.sismember("tags", query): #check if such a tag exists
            results+=list(event_tag.smembers(query))
            
    return results
    
def add_del_tag(add_del, eventid, tag_list): #add_del=+1 => add, add_del=-1 => delete
    event_tag=redis.Redis("localhost")
    event=str(Event.objects.get(pk=eventid))
    tag_list=[x.strip() for x in tag_list.split(',')]
    #to be done: split a single-word tag into smaller bits
    for t in tag_list:
        if add_del=+1:
            event_tag.sadd(t, event)
            event_tag.sadd("tags",t)
            if ' ' in t: #if added tag is "abc xyz", add tags for "abc" and "xyz" as well.
                for x in shlex.split(t):
                    event_tag.sadd(x, event)
                    event_tag.sadd("tags",x)
        if add_del=-1:
            event_tag.srem(t, event)
            event_tag.srem("tags", t)
    return
    
def edit_tag(eventid, oldtag, newtag):
    event_tag=redis.Redis("localhost")
    event=str(Event.objects.get(pk=eventid))
    event_tag.srem(oldtag, event)
    event_tag.srem("tags",oldtag)
    event_tag.sadd(newtag, event)
    event_tag.sadd("tags",newtag)
    return
