# -*- coding: utf-8 -*-
import re
from django import forms
from django.db import models as d_models
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe
from submissions.models import *
from chosen import forms as chosenforms
import settings

class TDPSubmissionForm(forms.ModelForm):
    class Meta:
        model = TDPSubmissions
        fields = ('tdp_upload',)
        
