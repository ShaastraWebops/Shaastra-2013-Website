from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime
import os

# Create your models here.
def upload_handler(model_name):
    def upload_func(instance, filename):
        return os.path.join(model_name, instance.name, filename)
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
    user = models.ForeignKey(User, unique = True)
    is_core = models.BooleanField(default = False)
    is_coord_of = models.ForeignKey(Event, default = None)
    
