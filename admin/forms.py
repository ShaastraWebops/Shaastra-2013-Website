from django import forms
from django.contrib.auth.models import Group, User
from users.models import UserProfile
from users.forms import AddUserForm, EditUserForm
import re 

alnum_re = re.compile(r'^[\w.-]+$') # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields=('name',)

class AddCoreForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('groups','username','email')
#        widgets={'password':forms.widgets.HiddenInput,}
