# -*- coding: utf-8 -*-
#We can use the same forms as last time for registation. We are not really changing anything here so.
#If we have to change anything it shouldn't be much of a problem
from django import forms
from django.forms import ModelForm
from django.db import models as d_models
import re 
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from  users import models

#from  recaptcha import fields as recaptcha_fields


#from  misc import util

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
'''            
class LoginForm(forms.Form):
    email=forms.EmailField(help_text='Your Shaastra 2011 username')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password')
    

class AddUserForm(ModelForm):
    
    first_name      = forms.CharField  (max_length=30,
                                       help_text='Enter your first name here.')
    last_name       = forms.CharField  (max_length=30,
                                       help_text='Enter your last name here.')
#    username       = forms.CharField  (max_length=30,
#                                       help_text='30 characters or fewer. Letters, numbers and @/./+/-/_ characters')
    email          = forms.EmailField (help_text='Enter your e-mail address. eg, someone@gmail.com')
    password       = forms.CharField  (min_length=6,
                                       max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter a password that you can remember')
    password_again = forms.CharField  (max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter the same password that you entered above')
#    college        = forms.CharField  (max_length=120,
#                                       widget=forms.TextInput(attrs={'id':'coll_input'}),
#                                       help_text='Select your college from the list. If it is not there, use the link below')
#    college_roll   = forms.CharField  (max_length=25,
#                                       help_text='Enter your college ID / roll number here.')
#    branch         = forms.CharField  (max_length=50,
#                                       widget=forms.TextInput(attrs={'id':'branch_input'}),
#                                       help_text='Select your branch from the list. If it does not show up, please select the "Other" option.')
#    recaptcha      = recaptcha_fields.ReCaptchaField (label='Show us that you are not a bot!',
#                                                      help_text='Enter the words shown in the space provided')
    
    class Meta:
        model = models.UserProfile
        fields={'gender','age','branch','mobile_number','college_roll','want_hospi'}
        #exclude = {'is_coord','coord_event','shaastra_id','activation_key','key_expires','UID','user',}
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_age(self):
	if (self.cleaned_data['age']>80 or self.cleaned_data['age']<12):
	    raise forms.ValidationError(u'Please enter an acceptable age (12 to 80)')
	else:
	    return self.cleaned_data['age']
	    
    def clean_mobile_number(self):
	if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
	    raise forms.ValidationError(u'Enter a valid mobile number')
	if models.UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number']):
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

class UserRegisterForm(ModelForm):
    
    first_name      = forms.CharField  (max_length=30,
                                       help_text='Enter your first name here.')
    last_name       = forms.CharField  (max_length=30,
                                       help_text='Enter your last name here.')
#    username       = forms.CharField  (max_length=30,
#                                       help_text='30 characters or fewer. Letters, numbers and @/./+/-/_ characters')
    email          = forms.EmailField (help_text='Enter your e-mail address. eg, someone@gmail.com')
#    college        = forms.CharField  (max_length=120,
#                                       widget=forms.TextInput(attrs={'id':'coll_input'}),
#                                       help_text='Select your college from the list. If it is not there, use the link below')
#    college_roll   = forms.CharField  (max_length=25,
#                                       help_text='Enter your college ID / roll number here.')
#    branch         = forms.CharField  (max_length=50,
#                                       widget=forms.TextInput(attrs={'id':'branch_input'}),
#                                       help_text='Select your branch from the list. If it does not show up, please select the "Other" option.')
#    recaptcha      = recaptcha_fields.ReCaptchaField (label='Show us that you are not a bot!',
#                                                      help_text='Enter the words shown in the space provided')
    
    class Meta:
        model = models.UserProfile
        fields={'gender','age','branch','mobile_number','college_roll','want_hospi'}
        #exclude = {'is_coord','coord_event','shaastra_id','activation_key','key_expires','UID','user',}
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

    def clean_age(self):
	if (self.cleaned_data['age']>80 or self.cleaned_data['age']<12):
	    raise forms.ValidationError(u'Please enter an acceptable age (12 to 80)')
	else:
	    return self.cleaned_data['age']
	    
    def clean_mobile_number(self):
	if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
	    raise forms.ValidationError(u'Enter a valid mobile number')
	if models.UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number']):
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

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')


    
    def clean_college(self):
        coll_input = self.cleaned_data['college']
        try:
            coll_name, coll_city = coll_input.rsplit(',',1)
            collchk = models.College.objects.get(name = coll_name, city=coll_city)
        except: 
            raise forms.ValidationError ("Invalid college name, or college does not exist. Please use add college form below to add your college if it does not already exist")
        if(collchk):
            return collchk
        else :
            raise forms.ValidationError ("The College that you entered Does not exist or was Not Right")
               
    def clean_college_roll(self):
        if (not alphanumric.search(self.cleaned_data['college_roll'])) or self.cleaned_data['college_roll'].isalpha():
           raise forms.ValidationError(u'Enter a valid roll number.')
        else:
           return self.cleaned_data['college_roll']
         
         
'''     
class EditUserForm(ModelForm):

    first_name = forms.CharField(max_length=50, help_text="Your first name")
    last_name = forms.CharField(max_length=50, help_text="Your last name")

    class Meta:
        model = models.UserProfile
        #fields=('first_name', 'last_name', 'gender', 'age', 'branch', 'mobile_number', 'college_roll', 'want_hospi', )
        #except = ('is_coord','coord_event')        
        exclude = ('user', 'UID', 'activation_key', 'key_expires', 'is_coord', 'access_token', )
    
    #Commented out for the saudi arabia issue
	
    def clean_mobile_number(self):
	if (len(self.cleaned_data['mobile_number'])!=10 or (self.cleaned_data['mobile_number'][0]!='7' and self.cleaned_data['mobile_number'][0]!='8' and self.cleaned_data['mobile_number'][0]!='9') or (not self.cleaned_data['mobile_number'].isdigit())):
	    raise forms.ValidationError(u'Enter a valid mobile number')
	else:
	  return self.cleaned_data['mobile_number']
	

    def clean_age(self):
        if self.cleaned_data['age'] < 12 or self.cleaned_data['age'] > 80: 
        # This line was:
        #     if self.age < 12 or self.age > 80:
        # For some reason, that was throwing an Attribute Error: 'EditUserForm' object has no attribute 'age'
            raise forms.ValidationError(u'You need to be over 12 and under 80 years of age to participate')
        return self.cleaned_data['age']
   
    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]
    
    def clean_college_roll(self):
        if (not alphanumric.search(self.cleaned_data['college_roll'])) or self.cleaned_data['college_roll'].isalpha():
           raise forms.ValidationError(u'Enter a valid roll number.')
        else:
           return self.cleaned_data['college_roll']
'''
class ResetPasswordForm(forms.Form):
    user = forms.IntegerField(widget = forms.HiddenInput)
    password = forms.CharField(min_length = 6, max_length = 30, widget = forms.PasswordInput, help_text = 'Enter a password that you can remember')
    password_again = forms.CharField(max_length = 30, widget = forms.PasswordInput, help_text = 'Enter the same password that you entered above')
    
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
          
class UsernameForm(forms.Form):
    username = forms.CharField(max_length = 50, help_text = 'Please enter your username')
    
    def clean_username(self):
        if 'username' in self.cleaned_data:
            try:
                User.objects.get(username = self.cleaned_data['username'])
            except User.DoesNotExist:
                raise forms.ValidationError('Invalid username')
        return self.cleaned_data['username']
'''
class AddCollegeForm (ModelForm):
    class Meta:
        model = models.College
        fields=('name','city','state')

