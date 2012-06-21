from django import forms
from users.models import UserProfile
from events.models import Event
from django.contrib.auth.models import Group

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event



