#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ValidationError
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):

    first_name = forms.CharField(help_text='Your first name')
    email = forms.EmailField(help_text='Email id')
    username = forms.RegexField(regex=r'^\w+$', max_length=30,
                                help_text='Username must contain only alphabets / digits'
                                )
    password = forms.CharField(widget=forms.PasswordInput,
                               help_text='Password must contain at least 6 characters'
                               , min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput,
            help_text='Confirm Password', min_length=6)

    def clean_username(self):
        data = self.cleaned_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError(u'Username already exists')

    def clean_confirm_password(self):
        data = self.cleaned_data
        pass1 = data['password']
        pass2 = data['confirm_password']
        if pass1 and pass2:
            if pass1 != pass2:
                raise forms.ValidationError(u'Passwords do not match')
        return self.cleaned_data['confirm_password']


