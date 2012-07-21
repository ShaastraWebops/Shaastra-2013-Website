from django import forms
from events.models import*
from django.forms import ModelForm
import os

class AddOptionForm(ModelForm):
    class Meta:
        model = MCQOption
        exclude = ('question',)

#class AddMCQForm(ModelForm):
#    class Meta:
#        model = ObjectiveQuestion
#        fields = ('q_number', 'title')

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
    text = forms.CharField(widget=forms.Textarea(attrs={'id':'niced_text','height':'200','width':'200'}))
    class Meta:
        model = Tab
        exclude = ('event',)
        
class MobAppWriteupForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'id':'niced_text','height':'200','width':'200'}))
    class Meta:
        model = MobAppTab
        exclude = ('event',)

class MCQForm(forms.Form):
    def __init__(self, mcq, options):
        super(MCQForm, self).__init__()
        ini_title, ini_q_no = "", ""
        if mcq: ini_title, ini_q_no = mcq.title, mcq.q_number  
        self.fields['q_no'] = forms.IntegerField(initial = ini_q_no)
        self.fields['title'] = forms.CharField(widget = forms.Textarea, initial = ini_title)
        index = 0
        import string
        alp = string.lowercase
        for option in options:
            self.fields['%s%s' % (option.id,option.option)] = forms.CharField(initial = '%s' % option.text,label = 'option %s:' % alp[index], max_length = 1000)
            index+=1
        self.fields['opt%s' % alp[index]] = forms.CharField(label = 'option %s:' % alp[index], max_length = 1000)

class UpdateForm(ModelForm):
    class Meta:
        model = Update
        widgets = {
            'event': forms.HiddenInput(),
        }
