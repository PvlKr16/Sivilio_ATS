"""Forms for user account management."""

from django import forms
from .models import User


class UserUpdateForm(forms.ModelForm):
    """Form for editing user accounts."""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple,
        }
