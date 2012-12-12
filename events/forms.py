#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from events.models import *
from django.forms import ModelForm
import os


class MCQForm(forms.Form):

    def __init__(self, mcq, options):
        super(MCQForm, self).__init__()
        (ini_title, ini_q_no) = ('', '')
        if mcq:
            (ini_title, ini_q_no) = (mcq.title, mcq.q_number)
        self.fields['q_no'] = forms.IntegerField(initial=ini_q_no)
        self.fields['title'] = forms.CharField(widget=forms.Textarea,
                initial=ini_title)
        index = 0
        import string
        alp = string.lowercase
        for option in options:
            self.fields['%s%s' % (option.id, option.option)] = \
                forms.CharField(initial='%s' % option.text,
                                label='option %s:' % alp[index],
                                max_length=1000)
            index += 1
        self.fields['opt%s' % alp[index]] = \
            forms.CharField(label='option %s:' % alp[index],
                            max_length=1000)


# no forms here. defined model forms in models itself.
