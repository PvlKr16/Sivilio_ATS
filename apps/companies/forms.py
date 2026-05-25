"""Forms for the Companies module."""

from django import forms
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
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email...',
            'class': 'form-control',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All statuses'),
            ('active',   'Active'),
            ('inactive', 'Inactive'),
            ('lead',     'Lead'),
            ('paused',   'Paused'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    payment_options = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All payment options'),
            ('50_50',   '50/50'),
            ('on_fact', 'По факту'),
            ('prepaid', 'Предоплата'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
