from django import forms
from models import SubEvent, Venue
from django.forms import ModelForm

class SubEventForm(ModelForm):
    class Meta:
        model = SubEvent
        fields = ('title', 'event', 'start_date_and_time', 'end_date_and_time', 'venue')
        widgets = {
            'event' : forms.HiddenInput(),  # The event field should be populated automatically depending on which coord requests the form.
        }

class EventUnlockForm(forms.Form):
    unlock_reason = forms.CharField(max_length = 1024, help_text = 'Please give reason for unlocking.')
    
class VenueForm(ModelForm):
    class Meta:
        model = Venue
