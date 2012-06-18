from django import forms
from django.contrib.auth.models import Group

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group

