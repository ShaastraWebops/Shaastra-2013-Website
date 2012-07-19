from django.forms import ModelForm
from portal.models import *
"""
To create a tuple with only one element make sure comma is present after 'information'
"""
class TextForm(ModelForm):
    class Meta:
        model = Topic
        fields=('information',)
        
class HomeForm(ModelForm):
    class Meta:
        model = Home
        fields=('info',)        
