"""Forms for the Events module."""

from django import forms
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()


class EventForm(forms.ModelForm):
    """Create / edit form for Event."""

    class Meta:
        model  = Event
        fields = [
            'event_type', 'candidate', 'vacancy', 'company',
            'event_date', 'event_time',
            'supervisor', 'notes',
        ]
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'candidate':  forms.Select(attrs={'class': 'form-select'}),
            'vacancy':    forms.Select(attrs={'class': 'form-select'}),
            'company':    forms.Select(attrs={'class': 'form-select'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes':      forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Required fields
        for f in ('event_type', 'candidate'):
            self.fields[f].required = True
            self.fields[f].widget.attrs['required'] = 'required'

        # Limit supervisor to users with role 'Supervisor'
        self.fields['supervisor'].queryset = User.objects.filter(
            role__name='Supervisor'
        ).order_by('last_name', 'first_name')

        # Order candidates alphabetically
        from apps.people.models import Person
        self.fields['candidate'].queryset = Person.objects.order_by(
            'last_name', 'first_name'
        )

        # Order vacancies by title
        from apps.vacancies.models import Vacancy
        self.fields['vacancy'].queryset = Vacancy.objects.select_related(
            'company'
        ).order_by('title')

        # Custom label for vacancy to show company name
        self.fields['vacancy'].label_from_instance = lambda v: f"{v.title} ({v.company})"


class EventSearchForm(forms.Form):
    """Filter / search form for events list."""

    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by candidate, vacancy...',
            'class': 'form-control',
        })
    )
    supervisor = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    vacancy = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    company = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    event_type = forms.MultipleChoiceField(
        required=False,
        choices=Event.event_type.field.choices,
        widget=forms.CheckboxSelectMultiple,
    )
    candidate = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.companies.models import Company
        from apps.vacancies.models import Vacancy
        from apps.people.models import Person
        self.fields['supervisor'].queryset = User.objects.filter(
            role__name='Supervisor'
        ).order_by('last_name', 'first_name')
        self.fields['vacancy'].queryset = Vacancy.objects.select_related(
            'company'
        ).order_by('title')
        self.fields['vacancy'].label_from_instance = lambda v: f"{v.title} ({v.company})"
        self.fields['company'].queryset = Company.objects.order_by('name')
        self.fields['candidate'].queryset = Person.objects.order_by(
            'last_name', 'first_name'
        )
