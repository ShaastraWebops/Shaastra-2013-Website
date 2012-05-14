import json, urllib

from django.db import models
from django.contrib.auth.models import User

class TwitterInfo(models.Model):
    user = models.OneToOneField(User)
    
    name    = models.CharField(max_length=15)
    id      = models.BigIntegerField(primary_key=True)
    
    token   = models.CharField(max_length=100)
    secret  = models.CharField(max_length=100)
    
    def get_twitter_profile(self):
        twitter_profile = urllib.urlopen('https://api.twitter.com/1/users/lookup.json?screen_name=%s,twitter&include_entities=false' % self.user.username)
        return json.load(twitter_profile) 
