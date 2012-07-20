from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from chosen import forms as chosenforms
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.cache import cache
import os

EVENT_CATEGORIES = (
	("Aerofest", "Aerofest"),
	("Coding", "Coding"),
	("Design and Build", "Design and Build"),
	("Involve", "Involve"),
	("Quizzes", "Quizzes"),
	("Online", "Online"),
	("Department Flagship", "Department Flagship"),
	("Spotlight", "Spotlight"),
	("Workshops", "Workshops"),
        ("Others", "Others"),
)

CATEGORY = (
    ("Update", "Update"),
    ("Announcement", "Announcement"),
    ("Expired", "Expired"),
)

# Create your models here.
def upload_handler(model_name):
    def upload_func(instance, filename):
        return os.path.join(model_name, instance.title, filename)
    return upload_func

class Tag(models.Model):
    name = models.CharField(max_length = 25)
    def __unicode__(self,*args,**kwargs):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length = 30)
    events_logo = models.FileField(upload_to = upload_handler('Events'), blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank = True, null = True)
    category = models.CharField(max_length=50,choices= EVENT_CATEGORIES)
    lock_status = models.CharField(default = 'cannot_be_locked', max_length = 20)
    unlock_reason = models.TextField(default = '', blank = True)
    registrable_online = models.BooleanField(default=False, help_text='Can participants register online?')
    begin_registration = models.BooleanField(default=False, help_text='Mark as True to begin online registration')
    has_questionnaire = models.BooleanField(default = False, help_text='Will the participant have to answer a questionnaire?')
    
    def __unicode__(self):
        return '%s' % self.title
    
class Update(models.Model):
    subject = models.CharField(max_length = 25)
    description = models.TextField()
    date = models.DateField(default = datetime.now)
    category = models.CharField(max_length = 15, choices = CATEGORY)
    event = models.ForeignKey(Event, null=True, blank=True)

class Tab(models.Model):
    event = models.ForeignKey(Event, blank = True, null = True)
    title = models.CharField(max_length = 30)
    text = models.TextField()
    pref = models.IntegerField(max_length=2,default = 0, blank=False)
    
#    def save(self):
#        cache.set(str(self.id)+"_event", str(self.event), 2592000)
#        cache.set(str(self.id)+"_title", str(self.title), 2592000)
#        cache.set(str(self.id)+"_text", str(self.text), 2592000)
#        cache.set(str(self.id)+"_pref", str(self.pref), 2592000)
#        super(Tab, self).save(*args, **kwargs)
        
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
    title = models.TextField(max_length=1500, blank = False)
    
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
    question = models.ForeignKey(ObjectiveQuestion, null = True, blank = True)
    option = models.CharField(max_length = 1)
    text = models.TextField(max_length = 1000)
    def __unicode__(self):
        return self.text
    
    class Meta:
        ordering = ['option']

class MobAppTab(models.Model):
    event = models.OneToOneField(Event, blank = True, null = True)
    text = models.TextField()
