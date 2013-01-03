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
        exclude = ('already_checkedin','mattresses',)

class AddMultipleRoomsForm(forms.Form):
    rooms = forms.FileField(required = True)
    
class SiteCSVRegnForm(forms.Form):
    new_registrations_file = forms.FileField(required = True)
    
class ShaastraIDForm(forms.Form):
    barcode = forms.CharField(required = False,help_text = 'Scan Barcode')
    shaastraID = forms.CharField(required = False,help_text = 'Enter Shaastra ID')
    email = forms.CharField(required = False,help_text = 'Enter Email ID')

class IndividualForm(ModelForm):
    room = chosenforms.ChosenModelChoiceField(queryset=AvailableRooms.objects.filter(already_checkedin__lt=F('max_number')).order_by('hostel').order_by('room_no'))
    class Meta:
        model = IndividualCheckIn
        fields = ('room',
                  'duration_of_stay',
                  'number_of_mattresses_given',
                  'mattress_room',
                  'shaastra_ID',
                  'first_name',
                  'last_name',
                  'phone_no',
                  'check_in_control_room',
                  'check_out_control_room',
                  'comments')        
    
class UserForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30,
                               help_text='Please select a username.',
                               label='Shaastra username')
    email = \
        forms.EmailField()

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
            )
            
class CreateTeamForm(forms.ModelForm):
    
    def clean_event(self):
        if 'event' in self.cleaned_data:
            event = self.cleaned_data['event']
            try:
                Event.objects.get(pk = event.id)
            except Event.DoesNotExist:
                raise forms.ValidationError('Not a valid event')
        return self.cleaned_data['event']
        
    def clean_leader_shaastra_ID(self):
        if 'leader_shaastra_ID' in self.cleaned_data:
            leader_shaastra_ID = self.cleaned_data['leader_shaastra_ID']
            try:
                UserProfile.objects.get(shaastra_id = leader_shaastra_ID)
            except UserProfile.DoesNotExist:
                raise forms.ValidationError('Not a vaild Shaastra ID')
        return self.cleaned_data['leader_shaastra_ID']
    
    def clean(self):
        data = self.cleaned_data
        if 'name' in data and 'event' in data:
            try:
                Team.objects.filter(event__id = data['event'].id).get(name__iexact = data['name'])
                raise forms.ValidationError('A team with the same name already exists for this event!')
            except Team.DoesNotExist:
                pass
        return data
        
    leader_shaastra_ID = forms.CharField(max_length = 10, help_text = 'The Shaastra ID of the team leader')
    
    class Meta:
        model = Team
        fields = ('name', 'event', 'leader_shaastra_ID')
        
class TeamNameForm(forms.Form):
    team_name = forms.CharField()

class TeamBillForm(forms.Form):
    number_of_participants=forms.IntegerField()
