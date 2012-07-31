from django.db import models
from events.models import Event

# Create your models here.

class EventFB(models.Model):
    event = models.ForeignKey(Event)
    desc  = models.CharField(max_length=500)
    
    def __unicode__(self):
        return '%s' % self.event.title