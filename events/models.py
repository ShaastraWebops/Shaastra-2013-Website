from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime
import os

# Create your models here.
def upload_handler(model_name):
    def upload_func(instance, filename):
        return os.path.join(model_name, instance.title, filename)
    return upload_func


class Question(models.Model):
    question = models.TextField()
    image = models.ImageField(upload_to = upload_handler('Events'))
    
class Tag(models.Model):
    name = models.CharField(max_length = 25)

class Category(models.Model):
    name = models.CharField(max_length = 25)
    
class Update(models.Model):
    subject = models.CharField(max_length = 25)
    description = models.TextField()
    date = models.DateField(default = datetime.now)

class Event(models.Model):
    title = models.CharField(max_length = 30)
    events_logo = models.ImageField(upload_to = upload_handler('Events'))
    questions = models.ManyToManyField(Question, blank = True, null = True)
    tags = models.ManyToManyField(Tag, blank = True, null = True)
    category = models.ForeignKey(Category, blank = True, null = True)
    updates = models.ManyToManyField(Update, blank = True, null = True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_core = models.BooleanField(default = False)
    is_coord_of = models.ForeignKey(Event, blank = True, null = True)
    
class Tab(models.Model):
    event = models.ForeignKey(Event, blank = True, null = True)
    title = models.CharField(max_length = 30)
    text = models.TextField()
    pref = models.IntegerField(max_length=2,default = 0, blank=False)
    class Meta:
        ordering = ['pref']

#tabfiles is not functional right now        
class TabFile(models.Model):
    name = models.CharField(max_length = 30)
    tabfile = models.FileField(upload_to = upload_handler('Events/TabFiles'))
    tab = models.ForeignKey(Tab, blank = True, null = True)
    
#tabfiles is not functional right now 
class TabFileForm(ModelForm):
    class Meta:
        model = TabFile
        exclude = ('tab',)
    
class EventAddForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title','events_logo','tags')
        
class TabAddForm(ModelForm):
    class Meta:
        model = Tab
        exclude = ('event',)
        

    
