from django import forms
from events.models import*
from django.forms import ModelForm
import os

class AddOptionForm(ModelForm):
    class Meta:
        model = MCQOption
        exclude = ('question',)

class AddMCQForm(ModelForm):
    class Meta:
        model = ObjectiveQuestion
        fields = ('q_number', 'title')

class AddSubjectiveQuestionForm(ModelForm):
    class Meta:
        model = SubjectiveQuestion
        fields = ('q_number', 'title')

class TabFileForm(ModelForm):
    class Meta:
        model = TabFile
        exclude = ('tab',)
    
class EventAddForm(ModelForm):
    tags = chosenforms.ChosenModelMultipleChoiceField(required = False,queryset = Tag.objects.all())
    class Meta:
        model = Event
        # fields = ('title','events_logo','tags')
        fields = ('title','events_logo', 'tags', 'lock_status', 'unlock_reason')
        widgets = {
            'lock_status' : forms.HiddenInput(),
            'unlock_reason' : forms.HiddenInput(),
        }        

class TabAddForm(ModelForm):
    class Meta:
        model = Tab
        exclude = ('event',)
        
class MobAppWriteupForm(ModelForm):
    class Meta:
        model = MobAppTab
        exclude = ('event',)

