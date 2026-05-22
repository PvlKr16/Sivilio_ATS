"""Forms for the People module."""

from django import forms
from .models import Person


def validate_cv(f):
    """Enforce PDF-only for CV uploads."""
    if f and hasattr(f, 'name') and not f.name.lower().endswith('.pdf'):
        raise forms.ValidationError('CV must be a PDF file.')
    return f


class PersonForm(forms.ModelForm):
    """Create / edit form for Person."""

    class Meta:
        model  = Person
        fields = [
            'avatar',
            'first_name', 'last_name', 'gender', 'birthdate',
            'profession', 'level', 'main_skill', 'skills',
            'english', 'education', 'work_experience',
            'salary_desired', 'salary_currency',
            'region', 'working_hours', 'working_place',
            'email', 'phone', 'linkedin', 'telegram',
            'status', 'notes', 'cv',
        ]
        widgets = {
            'birthdate':     forms.DateInput(attrs={'type': 'date'}),
            'gender':        forms.Select(attrs={'class': 'form-select'}),
            'level':         forms.Select(attrs={'class': 'form-select'}),
            'main_skill': forms.Select(attrs={'class': 'form-select', 'data-no-select2': ''}),
            'skills':        forms.CheckboxSelectMultiple(),
            'english':       forms.Select(attrs={'class': 'form-select'}),
            'profession':    forms.Select(attrs={'class': 'form-select'}),
            'region':        forms.Select(attrs={'class': 'form-select'}),
            'working_hours': forms.CheckboxSelectMultiple(),
            'working_place': forms.CheckboxSelectMultiple(),
            'salary_currency': forms.Select(attrs={'class': 'form-select'}),
            'status':        forms.Select(attrs={'class': 'form-select'}),
            'notes':         forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required fields
        for f in ('first_name', 'last_name'):
            self.fields[f].required = True
            self.fields[f].widget.attrs['required'] = 'required'

    def clean_cv(self):
        return validate_cv(self.cleaned_data.get('cv'))


class PersonSearchForm(forms.Form):
    """Filter form for the people list."""
    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email, phone...',
            'class': 'form-control',
        })
    )
    profession = forms.ModelChoiceField(
        queryset=None, required=False, empty_label='All professions',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    level = forms.ModelChoiceField(
        queryset=None, required=False, empty_label='All levels',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All statuses'), ('active', 'Active'), ('inactive', 'Inactive')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Profession, Level
        self.fields['profession'].queryset = Profession.objects.all()
        self.fields['level'].queryset      = Level.objects.all()
