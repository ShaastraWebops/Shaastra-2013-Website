# -*- coding: utf-8 -*-
#We can use the same forms as last time for registation. We are not really changing anything here so.
#If we have to change anything it shouldn't be much of a problem
import re 
from django import forms
from django.forms import ModelForm
from django.db import models as d_models
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from users.models import *

import settings

alnum_re = re.compile(r'^[\w.-]+$') # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")

GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        )

'''
class HorizRadioRenderer(forms.RadioSelect.renderer):
    #this overrides widget method to put radio buttons horizontally instead of vertically.
    def render(self):
            #Outputs radios
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
'''
            
class LoginForm(forms.Form):

    username=forms.CharField(help_text='Your Shaastra 2013 username')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password')

class BaseUserForm(forms.ModelForm):

    first_name      = forms.CharField  (max_length=30, help_text='Enter your first name here.')
    last_name       = forms.CharField  (max_length=30, help_text='Enter your last name here.')
    
    class Meta:
        model = UserProfile
    
    def clean_age(self):
	if (self.cleaned_data['age']>80 or self.cleaned_data['age']<12):
	    raise forms.ValidationError(u'Please enter an acceptable age (12 to 80)')
	else:
	    return self.cleaned_data['age']
	    
    def clean_mobile_number(self):
	if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
	    raise forms.ValidationError(u'Enter a valid mobile number')
	if UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number']):
	    pass    
	else:
	  return self.cleaned_data['mobile_number']
	raise forms.ValidationError('This mobile number is already registered')  
	  
    def clean_first_name(self):
	if not self.cleaned_data['first_name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['first_name']
	  
    def clean_last_name(self):
	if not self.cleaned_data['last_name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['last_name']

class AddUserForm(BaseUserForm):

    username        = forms.CharField  (max_length=30, help_text='Your Shaastra 2013 username')
    email           = forms.EmailField (help_text='Enter your e-mail address. eg, someone@gmail.com')
    password        = forms.CharField  (min_length=6,
                                       max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter a password that you can remember')
    password_again = forms.CharField  (max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter the same password that you entered above')
    
    class Meta(BaseUserForm.Meta):
        fields=('first_name', 'last_name', 'username', 'email', 'password', 'password_again', 'college', 'college_roll', 'gender', 'age', 'branch', 'mobile_number')
        #exclude = {'is_coord','coord_event','shaastra_id','activation_key','key_expires','UID','user',}

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]

class EditUserForm(BaseUserForm):

    class Meta(BaseUserForm.Meta):

        fields=('first_name', 'last_name', 'gender', 'age', 'branch', 'mobile_number', 'college', 'college_roll' )
        #exclude = ('user', 'facebook_id', 'activation_key', 'key_expires', 'is_coord', 'access_token', 'username', 'email',)

    def clean_mobile_number(self):
        if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
            pass	
        elif 'mobile_number' in self.changed_data:
            if UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number']):
                raise forms.ValidationError('This mobile number is already registered')
            else:
                return self.cleaned_data['mobile_number']
        raise forms.ValidationError(u'Enter a valid mobile number')
	


class AddCollegeForm (ModelForm):
    class Meta:
        model = College
        fields=('name','city','state')

