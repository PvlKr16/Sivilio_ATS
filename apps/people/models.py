"""
Models for the People module.

Reference models (also used by Vacancy):
  Gender, Level, Skill, WorkingHours, Region, WorkingPlace, Profession, English

Person-specific:
  Person
"""

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# ── Currency choices for salary ───────────────────────────────────────────────

class CurrencyChoices(models.TextChoices):
    USD = 'USD', 'USD ($)'
    EUR = 'EUR', 'EUR (€)'
    UAH = 'UAH', 'UAH (₴)'
    RUB = 'RUB', 'RUB (₽)'
    GBP = 'GBP', 'GBP (£)'


# ── Person status ─────────────────────────────────────────────────────────────

class PersonStatus(models.TextChoices):
    # ИСПРАВЛЕНО: ключи (значения БД) — обычные строки, только label через _()
    ACTIVE   = 'active',   _('Active')
    INACTIVE = 'inactive', _('Inactive')


# ════════════════════════════════════════════════════════════════════════════════
# Reference models — shared with Vacancy
# ════════════════════════════════════════════════════════════════════════════════

class Gender(models.Model):
    # ИСПРАВЛЕНО: verbose_name поля через _()
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Gender')
        verbose_name_plural = _('Genders')
        ordering = ['name']

    def __str__(self):
        return self.name


class Level(models.Model):
    # ИСПРАВЛЕНО: labels в choices через _()
    LEVEL_CHOICES = [
        ('junior',    _('Junior')),
        ('middle',    _('Middle')),
        ('senior',    _('Senior')),
        ('lead',      _('Lead')),
        ('head_of',   _('Head of')),
        ('architect', _('Architect')),
    ]
    name  = models.CharField(max_length=20, choices=LEVEL_CHOICES,
                             unique=True, verbose_name=_('Level'))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        ordering = ['order']

    def __str__(self):
        return self.get_name_display()


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Working Hours')
        verbose_name_plural = _('Working Hours')
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkingPlace(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Working Place')
        verbose_name_plural = _('Working Places')
        ordering = ['name']

    def __str__(self):
        return self.name


class English(models.Model):
    # ИСПРАВЛЕНО: labels через _()
    LEVEL_CHOICES = [
        ('a1', _('A1 — Beginner')),
        ('a2', _('A2 — Elementary')),
        ('b1', _('B1 — Intermediate')),
        ('b2', _('B2 — Upper-Intermediate')),
        ('c1', _('C1 — Advanced')),
        ('c2', _('C2 — Proficient')),
    ]
    name  = models.CharField(max_length=10, choices=LEVEL_CHOICES,
                             unique=True, verbose_name=_('Name'))
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_('Order'))

    class Meta:
        verbose_name = _('English Level')
        verbose_name_plural = _('English Levels')
        ordering = ['order']

    def __str__(self):
        return self.get_name_display()


# ════════════════════════════════════════════════════════════════════════════════
# Person
# ════════════════════════════════════════════════════════════════════════════════

class Person(models.Model):
    """
    HR candidate / contact record.
    All reference fields (Gender, Level, etc.) are shared with Vacancy.
    """

    # ── Identity ──────────────────────────────────────────────────────────────
    first_name = models.CharField(max_length=150, verbose_name=_('First Name'))
    last_name  = models.CharField(max_length=150, verbose_name=_('Last Name'))
    gender     = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Gender'))
    birthdate  = models.DateField(null=True, blank=True, verbose_name=_('Birthdate'))

    # ── Professional ──────────────────────────────────────────────────────────
    profession      = models.CharField(max_length=150, blank=True, verbose_name=_('Profession'))
    level           = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Level'))
    skills          = models.ManyToManyField(Skill, blank=True, related_name='people', verbose_name=_('Skills'))
    english         = models.ForeignKey(English, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('English'))
    education       = models.CharField(max_length=255, blank=True, verbose_name=_('Education'))
    work_experience = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('Work Experience (years)'))

    # ── Salary ────────────────────────────────────────────────────────────────
    salary_desired = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name=_('Salary Desired'),
    )
    salary_currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
        blank=True,
        verbose_name=_('Currency'),
    )

    # ── Location & schedule ───────────────────────────────────────────────────
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('Region'),
    )
    working_hours = models.ManyToManyField(
        WorkingHours, blank=True,
        verbose_name=_('Working Hours'),
    )
    working_place = models.ManyToManyField(
        WorkingPlace, blank=True,
        verbose_name=_('Working Place'),
    )

    # ── Contacts ──────────────────────────────────────────────────────────────
    # ИСПРАВЛЕНО: добавлены _() для email, linkedin, telegram
    email    = models.EmailField(unique=True, null=True, blank=True, verbose_name=_('E-mail'))
    phone    = models.CharField(max_length=50, blank=True, verbose_name=_('Phone'))
    linkedin = models.URLField(blank=True, verbose_name=_('LinkedIn'))
    telegram = models.CharField(max_length=100, blank=True, verbose_name=_('Telegram'))

    # ── Status & meta ─────────────────────────────────────────────────────────
    status = models.CharField(
        max_length=10,
        choices=PersonStatus.choices,
        default=PersonStatus.ACTIVE,
        verbose_name=_('Status'),
    )
    notes      = models.TextField(blank=True, verbose_name=_('Notes'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        ordering = ['last_name', 'first_name']
        permissions = [
            ('export_person', 'Can export people data'),
        ]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('people:detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self):
        parts = [self.first_name, self.last_name]
        letters = [p[0].upper() for p in parts if p]
        return ''.join(letters[:2]) if letters else '?'

    @property
    def salary_display(self):
        if self.salary_desired:
            return f"{self.salary_desired:,.0f} {self.salary_currency}"
        return '—'


# ════════════════════════════════════════════════════════════════════════════════
# PersonFile — multiple attachments per Person
# ════════════════════════════════════════════════════════════════════════════════

def person_file_upload_to(instance, filename):
    """Store files under people/<person_pk>/filename."""
    return f'people/{instance.person_id}/{filename}'


class PersonFile(models.Model):
    """CV file (PDF only) attached to a Person. Multiple files allowed."""

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Person'),
    )
    # ИСПРАВЛЕНО: verbose_name и help_text через _()
    file = models.FileField(
        upload_to=person_file_upload_to,
        verbose_name=_('CV (PDF)'),
        help_text=_('PDF files only'),
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Uploaded At'))

    class Meta:
        verbose_name        = _('Person File')
        verbose_name_plural = _('Person Files')
        ordering            = ['-uploaded_at']

    def __str__(self):
        import os
        return os.path.basename(self.file.name) if self.file else '—'

    @property
    def filename(self):
        import os
        return os.path.basename(self.file.name) if self.file else ''

    @property
    def extension(self):
        import os
        _, ext = os.path.splitext(self.file.name)
        return ext.lower().lstrip('.') if self.file else ''

    @property
    def is_pdf(self):
        return self.extension == 'pdf'
