"""Forms for the People module."""

from django import forms
from .models import Person, Level, English, Skill, Region, WorkingHours


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
            'first_name', 'last_name', 'gender', 'birthdate',
            'profession', 'level', 'skills',
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
            'skills':        forms.CheckboxSelectMultiple(),
            'english':       forms.Select(attrs={'class': 'form-select'}),
            'region':        forms.Select(attrs={'class': 'form-select'}),
            'working_hours': forms.CheckboxSelectMultiple(),
            'working_place': forms.CheckboxSelectMultiple(),
            'salary_currency': forms.Select(attrs={'class': 'form-select'}),
            'status':        forms.Select(attrs={'class': 'form-select'}),
            'notes':         forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('first_name', 'last_name'):
            self.fields[f].required = True
            self.fields[f].widget.attrs['required'] = 'required'

    def clean_cv(self):
        return validate_cv(self.cleaned_data.get('cv'))


class PersonSearchForm(forms.Form):
    """Filter form for the people list."""

    # ── Row 0: search bar (kept as-is) ────────────────────────────────────
    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, email, phone…',
            'class': 'form-control',
        })
    )

    # ── Row 1 ─────────────────────────────────────────────────────────────
    english = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label='English',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    created_from = forms.DateField(
        required=False, label='Created from',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    created_to = forms.DateField(
        required=False, label='Created to',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    exp_from = forms.IntegerField(
        required=False, label='Exp from', min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'From', 'class': 'form-control', 'min': '0',
        }),
    )
    exp_to = forms.IntegerField(
        required=False, label='Exp to', min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'To', 'class': 'form-control', 'min': '0',
        }),
    )
    salary_currency = forms.ChoiceField(
        required=False, label='Currency',
        choices=[
            ('', 'Any'),
            ('USD', 'USD ($)'),
            ('EUR', 'EUR (€)'),
            ('UAH', 'UAH (₴)'),
            ('RUB', 'RUB (₽)'),
            ('GBP', 'GBP (£)'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    salary_from = forms.IntegerField(
        required=False, label='Salary from', min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'From', 'class': 'form-control', 'min': '0',
        }),
    )
    salary_to = forms.IntegerField(
        required=False, label='Salary to', min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'To', 'class': 'form-control', 'min': '0',
        }),
    )

    # ── Row 2 ─────────────────────────────────────────────────────────────
    skills = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label='Skills',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    level = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label='Level',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    region = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label='Region',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )
    working_hours = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label='Working Hours',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'multi-check-list'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['english'].queryset       = English.objects.all()
        self.fields['skills'].queryset        = Skill.objects.all()
        self.fields['level'].queryset         = Level.objects.all()
        self.fields['region'].queryset        = Region.objects.all()
        self.fields['working_hours'].queryset = WorkingHours.objects.all()
