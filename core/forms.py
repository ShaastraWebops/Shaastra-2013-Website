from django import forms
from events.models import Event
from django.contrib.auth.models import User
from users.models import UserProfile
from chosen import forms as chosenforms
from events.models import *

class AddEventForm(forms.ModelForm):

    tags = chosenforms.ChosenModelMultipleChoiceField(required = False,queryset = Tag.objects.all())
    class Meta:
        model = Event
        # fields = ('title','events_logo','tags')
        fields = ('title','events_logo', 'tags', 'lock_status', 'unlock_reason')
        widgets = {
            'lock_status' : forms.HiddenInput(),
            'unlock_reason' : forms.HiddenInput(),
        }        

class AddCoordForm(forms.ModelForm):
    """
    This form is used to add/edit coords

    """
    event = chosenforms.ChosenModelChoiceField(required = False,queryset = Event.objects.all())
#    event= forms.ModelChoiceField(queryset=Event.objects.all(),empty_label='----------')

    class Meta:
        model = User
        fields=('username', 'email')

