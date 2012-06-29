from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from chosen import forms as chosenforms
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from events.VenueChoices import VENUE_CHOICES  # These are the choices for the venues where events can be held
                                               #TODO(Anant): Update the VenueChoices.py file with all venues for Shaastra 2013
import os

# Create your models here.
def upload_handler(model_name):
    def upload_func(instance, filename):
        return os.path.join(model_name, instance.title, filename)
    return upload_func

class Tag(models.Model):
    name = models.CharField(max_length = 25)
    def __unicode__(self,*args,**kwargs):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 25)
    
class Update(models.Model):
    subject = models.CharField(max_length = 25)
    description = models.TextField()
    date = models.DateField(default = datetime.now)

class Event(models.Model):
    title = models.CharField(max_length = 30)
    events_logo = models.ImageField(upload_to = upload_handler('Events'))
    tags = models.ManyToManyField(Tag, blank = True, null = True)
    category = models.ForeignKey(Category, blank = True, null = True)
    updates = models.ManyToManyField(Update, blank = True, null = True)
    lock_status = models.CharField(default = 'cannot_be_locked', max_length = 20)
    unlock_reason = models.TextField(default = '', blank = True)
    
    def __unicode__(self):
        return '%s' % self.title

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
            '''
            if subEvent.event.title == 'Contraptions':
                contrapVenue = subEvent.venue
                contrapStart = subEvent.start_date_and_time
                contrapEnd = subEvent.end_date_and_time
                selfVenue = self.venue
                selfStart = self.start_date_and_time
                selfEnd = self.end_date_and_time
                assert False
            '''
            if subEvent.venue != venue:
                continue  # No clash

            if subEvent.start_date_and_time >= end:  # Start date-time of subEvent is after end date-time of self
                continue  # No clash

            if subEvent.end_date_and_time <= start:  # End date-time of subEvent is before start date-time of self
                continue  # No clash
            
            # The events clash.
            # Must tell user from when to when the venue is booked.
            subEventClashMsgs.append(u'%s is unavailable from %s to %s.' % (subEvent.venue, subEvent.start_date_and_time, subEvent.end_date_and_time))

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

class Tab(models.Model):
    event = models.ForeignKey(Event, blank = True, null = True)
    title = models.CharField(max_length = 30)
    text = models.TextField()
    pref = models.IntegerField(max_length=2,default = 0, blank=False)
    
    def delete(self):
        file_list = self.tabfile_set.all()
        for f in file_list:
            f.delete()
        super(Tab, self).delete()
        
    class Meta:
        ordering = ['pref']
       
class TabFile(models.Model):
    title = models.CharField(max_length = 50)
    tab_file = models.FileField(upload_to = upload_handler('Events/TabFiles'))
    tab = models.ForeignKey(Tab, blank = True, null = True)
    url = models.CharField(max_length = 50)
    
    def delete(self):
        os.remove(self.tab_file.name)
        super(TabFile, self).delete()
        
class Question(models.Model):
    q_number = models.IntegerField(max_length=2) 
    title = models.CharField(max_length=1500, blank = False)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['q_number']
        
class SubjectiveQuestion(Question):
    event= models.ForeignKey(Event)

class ObjectiveQuestion(Question):
    event= models.ForeignKey(Event)
    
    def delete(self):
        options = self.mcqoption_set.all()
        for option in options:
            option.delete()
        super(ObjectiveQuestion, self).delete()

class MCQOption(models.Model):
    question = models.ForeignKey(ObjectiveQuestion)
    option = models.CharField(max_length = 1)
    text = models.TextField(max_length = 1000)
    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ['option']

class MobAppTab(models.Model):
    event = models.OneToOneField(Event, blank = True, null = True)
    text = models.TextField()
    
    

class AddOptionForm(ModelForm):
    class Meta:
        model = MCQOption
        exclude = ('question',)

class AddMCQForm(ModelForm):
    class Meta:
        model = ObjectiveQuestion
        fields = ('q_number', 'title')

class AddSubjectiveQuestionForm(ModelForm):
    class Meta:
        model = SubjectiveQuestion
        fields = ('q_number', 'title')

class TabFileForm(ModelForm):
    class Meta:
        model = TabFile
        exclude = ('tab',)
    
class EventAddForm(ModelForm):
    tags = chosenforms.ChosenModelMultipleChoiceField(required = False,queryset = Tag.objects.all())
    class Meta:
        model = Event
        # fields = ('title','events_logo','tags')
        fields = ('title','events_logo', 'tags', 'lock_status', 'unlock_reason')
        widgets = {
            'lock_status' : forms.HiddenInput(),
            'unlock_reason' : forms.HiddenInput(),
        }
        
class SubEventForm(ModelForm):
    class Meta:
        model = SubEvent
        fields = ('title', 'start_date_and_time', 'end_date_and_time', 'venue', 'event', )
        widgets = {
            'event' : forms.HiddenInput(),
        }
        
class EventUnlockForm(forms.Form):
    unlock_reason = forms.CharField(max_length = 1024, help_text = 'Please give reason for unlocking.')
'''    
    def clean(self):
        errors = []
        super(EventUnlockForm, self).clean()  # Calling clean method of the super class
        
        dirself = dir(self)
        assert False
        
        if self.unlock_reason == '':
            errors.append(u'The reason cannot be empty.')
            
        raise ValidationError(errors)
'''        

class TabAddForm(ModelForm):
    class Meta:
        model = Tab
        exclude = ('event',)
        
class MobAppWriteupForm(ModelForm):
    class Meta:
        model = MobAppTab
        exclude = ('event',)
        

    
