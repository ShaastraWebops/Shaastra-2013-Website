#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from django import forms
from django.forms import ModelForm
from django.db import models as d_models
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from users.models import *
from controlroom.models import *
from chosen import widgets as chosenwidgets
import settings

class AddRoomForm(ModelForm):
    class Meta:
        model = AvailableRooms

class AddMultipleRoomsForm(forms.Form):
    rooms = forms.FileField(required = True)
    
class ShaastraIDForm(forms.Form):
    shaastraID = forms.CharField(help_text = 'Enter Shaastra ID of participant')

class IndividualForm(ModelForm):
    class Meta:
        model = IndividualCheckIn
        widgets = {'room': chosenwidgets.ChosenSelect}
        #TODO:Display only available rooms
        
