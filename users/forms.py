#!/usr/bin/python
# -*- coding: utf-8 -*-

# We can use the same forms as last time for registation. We are not really changing anything here so.
# If we have to change anything it shouldn't be much of a problem

import re
from django import forms
from django.forms import ModelForm
from django.db import models as d_models
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from users.models import *
from chosen import forms as chosenforms

# from recaptcha import fields as recaptcha_fields

import settings

alnum_re = re.compile(r'^[\w.-]+$')  # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")

GENDER_CHOICES = ((1, 'Male'), (2, 'Female'))
BRANCH_CHOICES = (
    ('Arts', 'Arts'),
    ('Accounting', 'Accounting'),
    ('Applied Mechanics', 'Applied Mechanics'),
    ('Mechatronics', 'Mechatronics'),
    ('Aerospace Engineering', 'Aerospace Engineering'),
    ('Automobile Engineering', 'Automobile Engineering'),
    ('Biotech / Biochemical / Biomedical', 'Biotech / Biochemical / Biomedical'),
    ('Biology', 'Biology'),
    ('Ceramic Engineering', 'Ceramic Engineering'),
    ('Chemical Engineering', 'Chemical Engineering'),
    ('Chemistry', 'Chemistry'),
    ('Design', 'Design'),
    ('Engineering Design', 'Engineering Design'),
    ('Civil Engineering', 'Civil Engineering'),
    ('Computer Science and Engineering', 'Computer Science and Engineering'),
    ('Electronics and Communications Engineering', 'Electronics and Communications Engineering'),
    ('Electrical and Electronics Engineering', 'Electrical and Electronics Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Electronics and Instrumentation Engineering', 'Electronics and Instrumentation Engineering'),
    ('Engineering Physics', 'Engineering Physics'),
    ('Economics', 'Economics'),
    ('Fashion Technology', 'Fashion Technology'),
    ('Humanities and Social Sciences', 'Humanities and Social Sciences'),
    ('Industrial Production', 'Industrial Production'),
    ('Production', 'Production'),
    ('Information Technology and Information Science', 'Information Technology and Sciences'),
    ('Management', 'Management'),
    ('Manufacturing', 'Manufacturing'),
    ('Mathematics', 'Mathematics'),
    ('Metallurgy and Material Science', 'Metallurgy and Material Science'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Ocean Engineering and Naval Architecture', 'Ocean Engineering and Naval Architecture'),
    ('Physics', 'Physics'),
    ('Telecom', 'Telecom'),
    ('Textile Engineering', 'Textile Engineering'),
    ('Others', 'Others'),
)

class LoginForm(forms.Form):

    username = forms.CharField(help_text='Your Shaastra 2013 username')
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text='Your password')


class BaseUserForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:

        model = UserProfile

    # The following code is to clean the a age field and to ensure that age is between 12 and 80.
    # Age limit has now been removed as demanded in Issue #29. To add it back, uncomment the 
    # following and also add the help_text in the age field in the model.
    '''
    def clean_age(self):
        if self.cleaned_data['age'] > 80 or self.cleaned_datlease enter your current mobile number
a['age'] \
            < 12:
            raise forms.ValidationError(u'<p>Please enter an acceptable age (12 to 80)</p>'
                    )
        else:
            return self.cleaned_data['age']
    '''
    
    def clean_mobile_number(self):
        if len(self.cleaned_data['mobile_number']) != 10 \
            or self.cleaned_data['mobile_number'][0] != '7' \
            and self.cleaned_data['mobile_number'][0] != '8' \
            and self.cleaned_data['mobile_number'][0] != '9' \
            or not self.cleaned_data['mobile_number'].isdigit():
            raise forms.ValidationError(u'<p>Enter a valid mobile number</p>'
                    )
        if UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number'
                ]):
            pass
        else:
            return self.cleaned_data['mobile_number']
        raise forms.ValidationError('<p>This mobile number is already registered</p>'
                                    )

    def clean_first_name(self):
        if not self.cleaned_data['first_name'].replace(' ', ''
                ).isalpha():
            raise forms.ValidationError(u'<p>Names cannot contain anything other than alphabets.</p>'
                    )
        else:
            return self.cleaned_data['first_name']

    def clean_last_name(self):
        if not self.cleaned_data['last_name'].replace(' ', ''
                ).isalpha():
            raise forms.ValidationError(u'<p>Names cannot contain anything other than alphabets.</p>'
                    )
        else:
            return self.cleaned_data['last_name']


class AddUserForm(BaseUserForm):

    username = forms.CharField(max_length=30,
                               help_text='Please select a username.',
                               label='Shaastra username')
    email = \
        forms.EmailField()
    password = forms.CharField(min_length=6, max_length=30,
                               widget=forms.PasswordInput,
                               help_text='Enter a password that you can remember'
                               )
    password_again = forms.CharField(max_length=30,
            widget=forms.PasswordInput,
            help_text='Enter the same password that you entered above')

    branch = chosenforms.ChosenChoiceField(overlay="You major in...", choices = BRANCH_CHOICES)
#    college = chosenforms.ChosenChoiceField(overlay="You study at...", queryset=College.objects.all())

    class Meta(BaseUserForm.Meta):

        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password_again',
            'college',
            'college_roll',
            'gender',
            'age',
            'branch',
            'mobile_number',
            'want_hospi',
            )

        # exclude = {'is_coord','coord_event','shaastra_id','activation_key','key_expires','UID','user',}

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
            raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores'
                    )
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.'
                                    )

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.'
                                    )

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password' % self.prefix
            field_name2 = '%s-password_again' % self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'

        if self.data[field_name1] != '' and self.data[field_name1] \
            != self.data[field_name2]:
            raise forms.ValidationError('The entered passwords do not match.'
                    )
        else:
            return self.data[field_name1]


class EditUserForm(BaseUserForm):
    branch = chosenforms.ChosenChoiceField(overlay="You major in...", choices = BRANCH_CHOICES)
    class Meta(BaseUserForm.Meta):

        fields = (
            'first_name',
            'last_name',
            'gender',
            'age',
            'branch',
            'mobile_number',
            'college',
            'college_roll',
            'want_hospi',
            )

        # exclude = ('user', 'facebook_id', 'activation_key', 'key_expires', 'is_coord', 'access_token', 'username', 'email',)

    def clean_mobile_number(self):
        if len(self.cleaned_data['mobile_number']) != 10 \
            or self.cleaned_data['mobile_number'][0] != '7' \
            and self.cleaned_data['mobile_number'][0] != '8' \
            and self.cleaned_data['mobile_number'][0] != '9' \
            or not self.cleaned_data['mobile_number'].isdigit():
            raise forms.ValidationError(u'Enter a valid mobile number')
        elif 'mobile_number' in self.changed_data:
            if UserProfile.objects.filter(mobile_number=self.cleaned_data['mobile_number'
                    ]):
                raise forms.ValidationError('This mobile number is already registered'
                        )
            else:
                return self.cleaned_data['mobile_number']
        return self.cleaned_data['mobile_number']


class FacebookUserForm(BaseUserForm):

    username = forms.CharField(max_length=30,
                               help_text='Your Shaastra 2013 username')
    email = \
        forms.EmailField(help_text='Enter your e-mail address. eg, someone@gmail.com'
                         )

    class Meta(BaseUserForm.Meta):

        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'gender',
            'age',
            'college',
            'college_roll',
            'branch',
            'mobile_number',
            )

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
            raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores'
                    )
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.'
                                    )

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.'
                                    )


class AddCollegeForm(ModelForm):

    class Meta:

        model = College
        fields = ('name', 'city', 'state')

