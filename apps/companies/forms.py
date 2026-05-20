"""Forms for the Companies module."""

from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    """Main company creation/edit form."""

    class Meta:
        model = Company
        fields = [
            'name', 'email', 'phone', 'fax',
            'bank', 'bank_account',
            'pays_vat', 'is_tenant',
            'mandatary',
            'logo', 'obs',
        ]
        widgets = {
            'obs': forms.Textarea(attrs={'rows': 3}),
            'mandatary': forms.Select(attrs={'class': 'form-select'}),
        }


class CompanySearchForm(forms.Form):
    """Search/filter form for company list."""
    q = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email...',
            'class': 'form-control',
        })
    )
    pays_vat = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('1', 'Pays VAT'), ('0', 'No VAT')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    is_tenant = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('1', 'Tenant'), ('0', 'Non-tenant')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
