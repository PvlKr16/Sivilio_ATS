"""Forms for the Vacancies module."""

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Vacancy, VacancyStatus, CurrencyChoices
from apps.people.models import Level, English, WorkingHours

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
            'skills':          forms.SelectMultiple(),
            'working_place':   forms.SelectMultiple(),
            'working_hours':   forms.SelectMultiple(),
            'supervisors':     forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('title', 'company'):
            self.fields[f].required = True
            self.fields[f].widget.attrs['required'] = 'required'

        self.fields['supervisors'].queryset = User.objects.filter(
            role__name='Supervisor'
        ).order_by('last_name', 'first_name')


class VacancySearchForm(forms.Form):
    """Filter form for the vacancies list."""

    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': _('Search by title, company…'),
            'class': 'form-control',
        })
    )

    supervisors = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label=_('Supervisor'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    status = forms.MultipleChoiceField(
        required=False, label=_('Status'),
        choices=VacancyStatus.choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    company = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label=_('Company'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )

    salary_currency = forms.ChoiceField(
        required=False, label=_('Currency'),
        choices=[
            ('',    _('Any')),
            ('USD', 'USD ($)'),
            ('EUR', 'EUR (€)'),
            ('UAH', 'UAH (₴)'),
            ('RUB', 'RUB (₽)'),
            ('GBP', 'GBP (£)'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    salary_from = forms.IntegerField(
        required=False, label=_('Salary from'), min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': _('From'), 'class': 'form-control', 'min': '0',
        }),
    )
    salary_to = forms.IntegerField(
        required=False, label=_('Salary to'), min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': _('To'), 'class': 'form-control', 'min': '0',
        }),
    )
    level = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label=_('Level'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    english = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label=_('English'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    working_hours = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label=_('Working Hours'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.companies.models import Company
        self.fields['supervisors'].queryset = User.objects.filter(
            role__name='Supervisor'
        ).order_by('last_name', 'first_name')
        self.fields['company'].queryset       = Company.objects.all()
        self.fields['level'].queryset         = Level.objects.all()
        self.fields['english'].queryset       = English.objects.all()
        self.fields['working_hours'].queryset = WorkingHours.objects.all()
