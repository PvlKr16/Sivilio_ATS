"""Forms for the People module."""

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from .models import Person, PersonFile, Level, English, Skill, Region, WorkingHours


def validate_pdf(f):
    """Enforce PDF-only uploads."""
    if f and hasattr(f, 'name') and not f.name.lower().endswith('.pdf'):
        raise forms.ValidationError(_('Only PDF files are allowed.'))
    return f


# ── Single file row inside the formset ────────────────────────────────────────

class PersonFileForm(forms.ModelForm):
    class Meta:
        model  = PersonFile
        fields = ['file']

    def clean_file(self):
        return validate_pdf(self.cleaned_data.get('file'))


# One CV file max: max_num=1, extra=1 (always show the upload row if none saved yet)
PersonFileFormSet = inlineformset_factory(
    Person,
    PersonFile,
    form=PersonFileForm,
    extra=1,
    max_num=1,
    can_delete=True,
)


# ── Main person form ──────────────────────────────────────────────────────────

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
            'status', 'notes',
        ]
        widgets = {
            'birthdate':       forms.DateInput(attrs={'type': 'date'}),
            'gender':          forms.Select(attrs={'class': 'form-select'}),
            'level':           forms.Select(attrs={'class': 'form-select'}),
            'skills':          forms.CheckboxSelectMultiple(),
            'english':         forms.Select(attrs={'class': 'form-select'}),
            'region':          forms.Select(attrs={'class': 'form-select'}),
            'working_hours':   forms.CheckboxSelectMultiple(),
            'working_place':   forms.CheckboxSelectMultiple(),
            'salary_currency': forms.Select(attrs={'class': 'form-select'}),
            'status':          forms.Select(attrs={'class': 'form-select'}),
            'notes':           forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('first_name', 'last_name'):
            self.fields[f].required = True
            self.fields[f].widget.attrs['required'] = 'required'


# ── Search / filter form ──────────────────────────────────────────────────────

class PersonSearchForm(forms.Form):
    """Filter form for the people list."""

    q = forms.CharField(
        required=False, label='',
        widget=forms.TextInput(attrs={
            'placeholder': _('Search by name, email, phone…'),
            'class': 'form-control',
        })
    )

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
            'placeholder': _('From'), 'class': 'form-control', 'min': '0',
        }),
    )
    exp_to = forms.IntegerField(
        required=False, label='Exp to', min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': _('To'), 'class': 'form-control', 'min': '0',
        }),
    )
    salary_currency = forms.ChoiceField(
        required=False, label='Currency',
        choices=[
            ('', _('Currency')),
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
            'placeholder': _('From'), 'class': 'form-control', 'min': '0',
        }),
    )
    salary_to = forms.IntegerField(
        required=False, label='Salary to', min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': _('To'), 'class': 'form-control', 'min': '0',
        }),
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=None, required=False, label=_('Skills'),
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
