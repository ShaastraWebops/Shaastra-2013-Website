from django.forms import ModelForm
from portal.models import Topic
"""
To create a tuple with only one element make sure comma is present after 'information'
"""
class TextForm(ModelForm):
    class Meta:
        model = Topic
        fields=('information',)
