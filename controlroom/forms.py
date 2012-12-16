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

