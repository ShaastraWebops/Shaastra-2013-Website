from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.sitemaps import ping_google

from events.models import Event

from dtvpicker.VenueChoices import VENUE_CHOICES  # These are the choices for the venues where events can be held
                                                  #TODO(Anant): Update the VenueChoices.py file with all venues for Shaastra 2013

class SubEvent(models.Model):
    """
    A sub-event is, e.g. Prelims 1, Finals, Workshop 2, Lecture 3, etc., of an event.
    """
    title = models.CharField(max_length = 32, 
                             help_text = 'Title of the sub-event. E.g. "Prelims 1", "Finals", "Lecture 2", "Workshop 3", etc.', 
                             verbose_name = "Sub-Event Title")
    start_date_and_time = models.DateTimeField(blank = True, null = True, help_text = 'When will this sub-event start? (yyyy-mm-dd hh:mm:ss)')
    end_date_and_time = models.DateTimeField(blank = True, null = True, help_text = 'When will this sub-event end? (yyyy-mm-dd hh:mm:ss)')
    venue = models.CharField(max_length = 64, blank = True, null = True, help_text = 'Where will this sub-event be held?', choices = VENUE_CHOICES)
    #TODO(Anant): Update the VenueChoices.py file with all venues for Shaastra 2013
    event = models.ForeignKey(Event)
    last_modified = models.DateTimeField(editable = False)

    def __unicode__(self):
        return '%s' % (self.title,)
        
    def checkSubEventClash(self, venue, start, end):
        """
        Checks if the sub-event submitted clashes with any other sub-event (under any event) in the database.
        If they do clash, returns an error message that describes the venue and its booking time.
        """
        '''
        Logic:: How to check if two sub-events (say A and B) clash:
            if A.venue != B.venue:
                They don't clash
            elif A.start > B.end:
                They don't clash
            elif A.end < B.start:
                They don't clash
            else:
                They clash
        '''
        subEventList = SubEvent.objects.all()

        try:
            subEventList = subEventList.exclude(id = self.id)
        except:
            pass
            
        subEventClashMsgs = []
        
        for subEvent in subEventList:

            if subEvent.venue != venue:
                continue  # No clash

            if subEvent.start_date_and_time >= end:  # Start date-time of subEvent is after end date-time of self
                continue  # No clash

            if subEvent.end_date_and_time <= start:  # End date-time of subEvent is before start date-time of self
                continue  # No clash
            
            # The events clash.
            # Must tell user from when to when the venue is booked.
            subEventClashMsgs.append(u'%s is unavailable from %s to %s.' % (subEvent.venue, 
                                                                            subEvent.start_date_and_time, 
                                                                            subEvent.end_date_and_time))

        if subEventClashMsgs:
            return subEventClashMsgs
        return None

    def clean(self):
        """
        This method will work to clean the instance of SubEvent created.
        Validations to be performed:
            * The start of the sub-event must not be after the end.
            * The start of the sub-event cannot be the same as the end
            * The DTV of the sub-event must not clash with any other sub-event's DTV.
            * The last_modified field must be updated to the current date and time.
        """
        # References:
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#validating-objects
        # https://docs.djangoproject.com/en/dev/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
        # http://stackoverflow.com/questions/2117048/django-overriding-the-clean-method-in-forms-question-about-raising-errors
        
        errors = []

        super(SubEvent, self).clean()  # Calling clean method of the super class

        # The start of the sub-event must not be after the end.
        # The start of the sub-event cannot be the same as the end
        if self.start_date_and_time and self.end_date_and_time:
            # Ensures that both these fields are valid
            if self.start_date_and_time > self.end_date_and_time:
                errors.append(u'Surely the event cannot start after it has ended!')
            elif self.start_date_and_time == self.end_date_and_time:
                errors.append(u'Surely the start and end time cannot be the same!')
                
            # The DTV of the sub-event must not clash with any other sub-event's DTV.
            if self.venue:
                # Ensures that event is valid
                # Already checked validity of start and end dates and times
                subEventClashErrorMsg = self.checkSubEventClash(self.venue, self.start_date_and_time, self.end_date_and_time)
                if subEventClashErrorMsg is not None:
                    errors.extend(subEventClashErrorMsg)
                    
        # The sub-event's title must be unique under its event.
        if self.title:
            # Ensures that the title is valid
            subEventList = SubEvent.objects.filter(event = self.event)
            if self.id:
                subEventList = subEventList.exclude(id = self.id)
            for subEvent in subEventList:
                if subEvent.title == self.title:
                    errors.append(u'You already have a sub-event with the name "%s".' % subEvent.title)
                    break

        if errors:
            raise ValidationError(errors)
                    
        # The last_modified field must be updated to the current date and time.
        self.last_updated = datetime.now()

    def save(self, force_insert=False, force_update=False):
	super(SubEvent, self).save(force_insert, force_update)
	try:
		ping_google()
	except Exception:
		pass

