from haystack.indexes import *
from haystack import site
from events.models import Event, Tab

class NoteIndex_tabs(SearchIndex):
    text = CharField(document=True, use_template=True)
    tabtext = CharField(model_attr='text')

class NoteIndex_events(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = EdgeNgramField(model_attr='title')
    category = EdgeNgramField(model_attr='category')
    
site.register(Tab, NoteIndex_tabs)
site.register(Event, NoteIndex_events)

