from django.db import models
from users.models import *
from events.models import *
from django.forms import ModelForm

# Create your models here.

class BaseSubmission(models.Model):
    event = models.ForeignKey(Event,null=False)
    # Additional features. 
    submitted = models.BooleanField()
    interesting = models.BooleanField(default=False,blank = True)
    sub_read = models.BooleanField(default=False,blank = True)
    selected = models.BooleanField(default=False,blank = True)
    score = models.FloatField(null=True, blank=True)
    rank = models.IntegerField(null=True,blank=True)
    is_new = models.BooleanField(default=True, blank=True)
    modified = models.BooleanField(default=False, blank=True)
    class Meta:
        ordering = ['id']

class IndividualSubmission(BaseSubmission):
    participant = models.ForeignKey(UserProfile)
    class Meta:
        ordering = ['id']
        
class Answer_Text(models.Model):
    question = models.ForeignKey(SubjectiveQuestion)
    text = models.TextField(blank = True, null = True)
    submission = models.ForeignKey(BaseSubmission)
    class Meta:
        ordering = ['id',]

class Answer_MCQ(models.Model):
    question = models.ForeignKey(ObjectiveQuestion)
    choice = models.ForeignKey(MCQOption, blank = True, null = True)
    submission = models.ForeignKey(BaseSubmission)
    class Meta:
        ordering = ['id',]
    def __unicode__(self):
        return self.choice.text
        
class Answer_Text_Form(ModelForm):
    text = forms.CharField(widget = forms.Textarea, label = '',)
    
    class Meta:
        model = Answer_Text
        exclude = ('question', 'submission')
                
class Answer_MCQ_Form(ModelForm):
    choice = forms.ModelMultipleChoiceField(queryset = MCQOption.objects.all(), widget = forms.RadioSelect, label = '')
    
    class Meta:
        model = Answer_MCQ
        exclude = ('question', 'submission')
        
    def __init__(self,*args, **kwargs):
        queryset = kwargs.pop('queryset')
        super(Answer_MCQ_Form, self).__init__(*args,**kwargs)
        self.fields['choice'].queryset = queryset
        print dir(self.fields['choice'].initial)
        
    

