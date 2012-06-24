from django import forms
from django.contrib.auth.models import Group, User
from users.forms import AddUserForm

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group

class AddCoreForm(AddUserForm):
    group= forms.ModelChoiceField(queryset=Group.objects.all(),empty_label='----------')
    class Meta(AddUserForm.Meta):
        fields=('group','first_name','last_name','gender','age','college_roll','mobile_number','email')

