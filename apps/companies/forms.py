"""Forms for the Companies module."""

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Company


class CompanyForm(forms.ModelForm):
    """Create / edit form for Company."""

    class Meta:
        model  = Company
        fields = [
            'name', 'email', 'phone', 'contact_person',
            'payment_options', 'amount', 'status', 'notes',
        ]
        widgets = {
            'payment_options': forms.Select(attrs={'class': 'form-select'}),
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'notes':           forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['name'].widget.attrs['required'] = 'required'


class CompanySearchForm(forms.Form):
    """Filter form for the company list."""
    q = forms.CharField(
        required=False, label=_('Search'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Search by name, email...'),
            'class': 'form-control',
        })
    )
    status = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('active',   _('Active')),
            ('inactive', _('Inactive')),
            ('lead',     _('Lead')),
            ('paused',   _('Paused')),
        ],
        widget=forms.CheckboxSelectMultiple,
    )
    payment_options = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('50_50',   '50/50'),
            ('on_fact', _('After')),
            ('prepaid', _('Prepayment')),
        ],
        widget=forms.CheckboxSelectMultiple,
    )
    