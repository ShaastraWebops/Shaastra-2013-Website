from django import forms
from django.contrib.auth.models import Group, User
from users.models import UserProfile

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields=('name',)

class AddCoreForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('groups','username','email')
#        widgets={'password':forms.widgets.HiddenInput,}
