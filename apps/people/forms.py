"""Forms for the People module."""

from django import forms
from .models import Person, Education, Work


class PersonForm(forms.ModelForm):
    """Main person creation/edit form."""

    class Meta:
        model = Person
        fields = [
            'title', 'name', 'appellative', 'gender',
            'uid', 'email', 'phone', 'birthday',
            'company', 'position', 'status',
            'avatar', 'obs',
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'obs': forms.Textarea(attrs={'rows': 3}),
            'title': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class PersonSearchForm(forms.Form):
    """Search/filter form for people list."""
    q = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email, position...',
            'class': 'form-control',
        })
    )
    company = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='All companies',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='All statuses',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        from apps.companies.models import Company
        from .models import PeopleStatus
        self.fields['company'].queryset = Company.objects.all()
        self.fields['status'].queryset = PeopleStatus.objects.filter(is_active=True)


class EducationForm(forms.ModelForm):
    """Form for education records."""

    class Meta:
        model = Education
        fields = ['level', 'institution', 'specialization', 'year_start', 'year_end', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'level': forms.Select(attrs={'class': 'form-select'}),
        }


class WorkForm(forms.ModelForm):
    """Form for work experience records."""

    class Meta:
        model = Work
        fields = ['employer', 'position', 'date_start', 'date_end', 'is_current', 'notes']
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_end': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
