# Create your models here.
from django.db import models
from django.contrib import admin

#Allows for updating status of event
STATUS_CHOICES = (
    ('s', 'Sold'),
    ('a', 'Available'),
)
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    url_name = models.CharField(max_length=30, blank=True)
    
    class Meta:
    	verbose_name_plural = "categories"
    	
    def get_events(self):
        return self.events.all()
    get_events.short_description = 'Events'
    
    def __unicode__(self):
        return self.name
    
class Event(models.Model):
    category = models.ForeignKey(Category, related_name = 'events')
    title = models.CharField(max_length=30, unique=True)
    about = models.TextField(null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
 
    def __unicode__(self):
        return self.title
"""
Image classes to add any number of
images for a category/event
"""
        
class CategoryImage(models.Model):
    name=models.CharField(max_length=30, blank=True)
    image=models.ImageField(upload_to='category',null=True,blank=True)
    category=models.ForeignKey(Category, related_name = 'categoryimages')
    def __unicode__(self):
        return self.name

class EventImage(models.Model):
    name=models.CharField(max_length=30, blank=True)
    image=models.ImageField(upload_to='event',null=True,blank=True)
    event=models.ForeignKey(Event, related_name = 'eventimages')
    def __unicode__(self):
        return self.name
