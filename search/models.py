from django.db import models

class Tag(models.Model):
    tag=models.CharField(max_length=100, unique=True)
        
    def __unicode__(self):
        return self.tag
        
class Event(models.Model):
    name=models.CharField(max_length=100, unique=True)
    tag=models.ManyToManyField(Tag)
        
    def __unicode__(self):
        return self.name

