from haystack.indexes import *
from haystack import site
from events.models import *
from django.template.defaultfilters import slugify

class NoteIndexTabs(SearchIndex):
    text = CharField(document=True, use_template=True)
    tabtext = CharField(model_attr='text')
    title = CharField(model_attr='title')
    event = CharField(model_attr='event', default=Event.objects.all()[1])

    def prepare_event(self,obj):
        try:
            if(obj.event.title):
                return obj.event.title
        except:
            pass
        
            
class NoteIndexEvents(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = EdgeNgramField(model_attr='title')
    category = EdgeNgramField(model_attr='category')
    url= CharField()
    
    def prepare_url(self,obj):
        try:
            return "#events/%s/tab/%s" %(slugify(obj.title),slugify(obj.tab_set.all()[0].title))
        except:
            return "#events/%s/tab" %slugify(obj.title)
               
site.register(Tab, NoteIndexTabs)
site.register(Event, NoteIndexEvents)

