"""Forms for user account management and self-service profile editing."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User


# ── Auth by e-mail ─────────────────────────────────────────────────

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )

# ── Shared validation helpers ─────────────────────────────────────────────────

def validate_avatar(f):
    """Enforce 3 MB limit on avatar uploads."""
    if f and f.size > 3 * 1024 * 1024:
        raise forms.ValidationError('Avatar file must be smaller than 3 MB.')
    return f


def validate_cv(f):
    """Enforce PDF-only for CV uploads."""
    if f:
        name = getattr(f, 'name', '')
        if not name.lower().endswith('.pdf'):
            raise forms.ValidationError('CV must be a PDF file.')
    return f


# ── Create user (admin / staff use) ──────────────────────────────────────────

class UserCreateForm(UserCreationForm):
    """Full creation form used in the admin-facing user management page."""

    class Meta:
        model  = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'viber', 'telegram',
            'role', 'status', 'works_since',
            'avatar', 'cv',
            'is_active', 'is_staff',
        ]
        widgets = {
            'works_since': forms.DateInput(attrs={'type': 'date'}),
            'role':        forms.Select(attrs={'class': 'form-select'}),
            'status':      forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('first_name', 'last_name', 'email', 'role'):
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['required'] = 'required'

    def clean_avatar(self):
        return validate_avatar(self.cleaned_data.get('avatar'))

    def clean_cv(self):
        return validate_cv(self.cleaned_data.get('cv'))


# ── Edit user ─────────────────────────────────────────────────────────────────

class UserUpdateForm(forms.ModelForm):
    """Edit form for an existing user — no password field."""

    class Meta:
        model  = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'viber', 'telegram',
            'role', 'status', 'works_since',
            'avatar', 'cv',
            'is_active', 'is_staff',
        ]
        widgets = {
            'works_since': forms.DateInput(attrs={'type': 'date'}),
            'role':        forms.Select(attrs={'class': 'form-select'}),
            'status':      forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('first_name', 'last_name', 'email', 'role'):
            self.fields[field_name].required = True
            self.fields[field_name].widget.attrs['required'] = 'required'

    def clean_avatar(self):
        return validate_avatar(self.cleaned_data.get('avatar'))

    def clean_cv(self):
        return validate_cv(self.cleaned_data.get('cv'))


# ── Self-service profile ──────────────────────────────────────────────────────

class ProfileUpdateForm(forms.ModelForm):
    """
    Restricted form for the 'My Profile' page.
    Users can update personal details but NOT their role, status or permissions.
    """

    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name', 'email',
            'phone', 'viber', 'telegram',
            'avatar', 'cv',
        ]
        widgets = {
            'avatar': forms.ClearableFileInput(),
            'cv':     forms.ClearableFileInput(),
        }

    def clean_avatar(self):
        return validate_avatar(self.cleaned_data.get('avatar'))

    def clean_cv(self):
        return validate_cv(self.cleaned_data.get('cv'))
