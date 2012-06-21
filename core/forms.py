from django import forms
from events.models import Event

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude=('events_logo','questions','tags','category','updates',)


