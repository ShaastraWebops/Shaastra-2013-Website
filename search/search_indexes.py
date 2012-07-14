import datetime
from haystack import *
from search.models import *
from haystack import site
from haystack import indexes
from haystack import *
from haystack.indexes import *

class EventIndex(SearchIndex):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    
    name_auto = indexes.EdgeNgramField(model_attr='name')
    def prepare(self, obj):
		self.prepared_data = super(EventIndex, self).prepare(obj)
		self.prepared_data['text'] = obj.name
		return self.prepared_data
    def get_model(self):
        return Event

    def index_queryset(self):

    
        return Event.objects.all()
site.register(Event,EventIndex)

