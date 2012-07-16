from django import forms
from django.contrib.auth.models import Group, User
from users.models import UserProfile
from chosen import widgets as chosenwidgets

class AddGroupForm(forms.ModelForm):
    """
    This form is used to add/edit groups

    """
    class Meta:
        model = Group
        fields=('name',)

class AddCoreForm(forms.ModelForm):
    """
    This form is used to add/edit cores

    """
    class Meta:
        model = User
        fields=('groups','username','email')
        widgets={'groups':chosenwidgets.ChosenSelect,}
