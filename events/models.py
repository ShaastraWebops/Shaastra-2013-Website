from django.contrib.sites import *
from django.contrib.sitemaps import *
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from chosen import forms as chosenforms
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
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

    def save(self, force_insert=False, force_update=False):
	super(Event, self).save(force_insert, force_update)
	try:
		ping_google()
	except Exception:
		pass

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

class TabAddForm(ModelForm):
    class Meta:
        model = Tab
        exclude = ('event',)
        
class MobAppWriteupForm(ModelForm):
    class Meta:
        model = MobAppTab
        exclude = ('event',)
        

    
