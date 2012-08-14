from haystack.indexes import *
from haystack import site
from events.models import *

class NoteIndexTabs(SearchIndex):
    text = CharField(document=True, use_template=True)
    tabtext = CharField(model_attr='text')

class NoteIndexEvents(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = EdgeNgramField(model_attr='title')
    category = EdgeNgramField(model_attr='category')
    
site.register(Tab, NoteIndexTabs)
site.register(Event, NoteIndexEvents)

