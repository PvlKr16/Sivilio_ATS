"""Forms for the Vacancies module."""

from django import forms
from django.contrib.auth import get_user_model
from .models import Vacancy

User = get_user_model()


class VacancyForm(forms.ModelForm):
    """Create / edit form for Vacancy."""

    class Meta:
        model  = Vacancy
        fields = [
            'status', 'company', 'title',
            'skills',
            'salary_offered', 'salary_currency',
            'level', 'english',
            'working_place', 'working_hours',
            'screening',
            'for_freelancers',
            'supervisors',
        ]
        widgets = {
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'company':         forms.Select(attrs={'class': 'form-select'}),
            'salary_currency': forms.Select(attrs={'class': 'form-select'}),
            'level':           forms.Select(attrs={'class': 'form-select'}),
            'english':         forms.Select(attrs={'class': 'form-select'}),
            'screening':       forms.Textarea(attrs={'rows': 4}),
            # M2M — rendered via Select2 in template
            'skills':          forms.SelectMultiple(),
            'working_place':   forms.SelectMultiple(),
            'working_hours':   forms.SelectMultiple(),
            'supervisors':     forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required fields
        for f in ('title', 'company'):
            self.fields[f].required = True
            self.fields[f].widget.attrs['required'] = 'required'

        # Limit supervisors to users with role 'Supervisor'
        self.fields['supervisors'].queryset = User.objects.filter(
            role__name='Supervisor'
        ).order_by('last_name', 'first_name')


class VacancySearchForm(forms.Form):
    """Filter form for the vacancies list."""
    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by title, company...',
            'class': 'form-control',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All statuses'),
                 ('in_progress', 'В работе'),
                 ('stop', 'Стоп')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    company = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='All companies',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    for_freelancers = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('1', 'Freelancers'), ('0', 'Not freelancers')],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.companies.models import Company
        self.fields['company'].queryset = Company.objects.all()
