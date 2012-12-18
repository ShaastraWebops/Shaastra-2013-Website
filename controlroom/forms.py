#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django import forms
from django.forms import ModelForm
from django.db.models import F
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from users.models import *
from controlroom.models import *
from chosen import forms as chosenforms
from chosen import widgets as chosenwidgets
import settings
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


class AddRoomForm(ModelForm):
    class Meta:
        model = AvailableRooms
        exclude = ('already_checkedin',)

class AddMultipleRoomsForm(forms.Form):
    rooms = forms.FileField(required = True)
    
class ShaastraIDForm(forms.Form):
    shaastraID = forms.CharField(help_text = 'Enter Shaastra ID of participant')

class IndividualForm(ModelForm):
    room = chosenforms.ChosenModelChoiceField(queryset=AvailableRooms.objects.filter(already_checkedin__lt=F('max_number')).order_by('hostel'))
    class Meta:
        model = IndividualCheckIn

class UserForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30,
                               help_text='Please select a username.',
                               label='Shaastra username')
    email = \
        forms.EmailField()
    password = forms.CharField(min_length=6, max_length=30,
                               widget=forms.PasswordInput,
                               help_text='Passwords need to be atleast 6 characters long.'
                               )
    password_again = forms.CharField(max_length=30,
            widget=forms.PasswordInput,
            help_text='Enter the same password that you entered above')

    branch = chosenforms.ChosenChoiceField(overlay="You major in...", choices = BRANCH_CHOICES)
    college = chosenforms.ChosenModelChoiceField(overlay="You study at...", queryset=College.objects.all())
    class Meta:
        model = UserProfile
        fields = (
            'college_roll',
            'gender',
            'age',
            'branch',
            'mobile_number',
            'want_accomodation',
            )
