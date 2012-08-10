from haystack.indexes import *
from haystack import site
from events.models import Event

class NoteIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    title = EdgeNgramField(model_attr='title')
    category = EdgeNgramField(model_attr='category')
    
site.register(Event, NoteIndex)
