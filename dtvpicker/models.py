from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.sitemaps import ping_google

from events.models import Event

from dtvpicker.VenueChoices import BLOCK_CHOICES

class Venue(models.Model):
    """
    The venue model is responsible for storing all the venues where events can be held.
    Venues are grouped under blocks.
    Ex: CRC 101-103, 201-205, 301-305 come under the CRC block.
    """
    title = models.CharField(max_length = 32, verbose_name = 'Venue Name')
    block = models.CharField(max_length = 8, choices = BLOCK_CHOICES)
    
    def __unicode__(self):
        return '%s' % (self.title,)
        
class SubEvent(models.Model):
    """
    A sub-event is, e.g. Prelims 1, Finals, Workshop 2, Lecture 3, etc., of an event.
    """
    title = models.CharField(max_length = 32, 
                             help_text = 'Title of the sub-event. E.g. "Prelims 1", "Finals", "Lecture 2", "Workshop 3", etc.', 
                             verbose_name = "Sub-Event Title")
    start_date_and_time = models.DateTimeField(blank = True, null = True, help_text = 'When will this sub-event start? (yyyy-mm-dd hh:mm:ss)')
    end_date_and_time = models.DateTimeField(blank = True, null = True, help_text = 'When will this sub-event end? (yyyy-mm-dd hh:mm:ss)')
    venue = models.ManyToManyField(Venue, blank = True, null = True, help_text = 'Where will this sub-event be held?')
    event = models.ForeignKey(Event)
    last_modified = models.DateTimeField(editable = False, auto_now = True)

    def __unicode__(self):
        return '%s' % (self.title,)

    def save(self, force_insert=False, force_update=False):
	super(SubEvent, self).save(force_insert, force_update)
	try:
		ping_google()
	except Exception:
		pass

