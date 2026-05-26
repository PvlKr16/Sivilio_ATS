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


# ── Currency choices for salary ───────────────────────────────────────────────

class CurrencyChoices(models.TextChoices):
    USD = 'USD', 'USD ($)'
    EUR = 'EUR', 'EUR (€)'
    UAH = 'UAH', 'UAH (₴)'
    RUB = 'RUB', 'RUB (₽)'
    GBP = 'GBP', 'GBP (£)'


# ── Person status ─────────────────────────────────────────────────────────────

class PersonStatus(models.TextChoices):
    ACTIVE   = 'active',   'Active'
    INACTIVE = 'inactive', 'Inactive'


# ════════════════════════════════════════════════════════════════════════════════
# Reference models — shared with Vacancy
# ════════════════════════════════════════════════════════════════════════════════

class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Gender')

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'
        ordering = ['name']

    def __str__(self):
        return self.name


class Level(models.Model):
    LEVEL_CHOICES = [
        ('junior',     'Junior'),
        ('middle',     'Middle'),
        ('senior',     'Senior'),
        ('lead',       'Lead'),
        ('head_of',    'Head of'),
        ('architect',  'Architect'),
    ]
    name  = models.CharField(max_length=20, choices=LEVEL_CHOICES,
                             unique=True, verbose_name='Level')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'
        ordering = ['order']

    def __str__(self):
        return self.get_name_display()


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Skill')

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkingHours(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Working Hours')

    class Meta:
        verbose_name = 'Working Hours'
        verbose_name_plural = 'Working Hours'
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Region')

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkingPlace(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Working Place')

    class Meta:
        verbose_name = 'Working Place'
        verbose_name_plural = 'Working Places'
        ordering = ['name']

    def __str__(self):
        return self.name


class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Profession')

    class Meta:
        verbose_name = 'Profession'
        verbose_name_plural = 'Professions'
        ordering = ['name']

    def __str__(self):
        return self.name


class English(models.Model):
    LEVEL_CHOICES = [
        ('a1', 'A1 — Beginner'),
        ('a2', 'A2 — Elementary'),
        ('b1', 'B1 — Intermediate'),
        ('b2', 'B2 — Upper-Intermediate'),
        ('c1', 'C1 — Advanced'),
        ('c2', 'C2 — Proficient'),
    ]
    name  = models.CharField(max_length=10, choices=LEVEL_CHOICES,
                             unique=True, verbose_name='English Level')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'English Level'
        verbose_name_plural = 'English Levels'
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
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name  = models.CharField(max_length=150, verbose_name='Last Name')
    gender     = models.ForeignKey(
        Gender, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Gender',
    )
    birthdate = models.DateField(null=True, blank=True, verbose_name='Birthdate')

    # ── Professional ──────────────────────────────────────────────────────────
    profession = models.ForeignKey(
        Profession, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Profession',
    )
    level = models.ForeignKey(
        Level, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Level',
    )
    main_skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='main_skill_people',
        verbose_name='Main Skill',
    )
    skills = models.ManyToManyField(
        Skill, blank=True,
        related_name='people',
        verbose_name='Skills',
    )
    english = models.ForeignKey(
        English, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='English',
    )
    education = models.CharField(
        max_length=255, blank=True, verbose_name='Education',
    )
    work_experience = models.PositiveSmallIntegerField(
        null=True, blank=True,
        verbose_name='Work Experience (years)',
    )

    # ── Salary ────────────────────────────────────────────────────────────────
    salary_desired  = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        verbose_name='Salary Desired',
    )
    salary_currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
        blank=True,
        verbose_name='Currency',
    )

    # ── Location & schedule ───────────────────────────────────────────────────
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Region',
    )
    working_hours = models.ManyToManyField(
        WorkingHours, blank=True,
        verbose_name='Working Hours',
    )
    working_place = models.ManyToManyField(
        WorkingPlace, blank=True,
        verbose_name='Working Place',
    )

    # ── Contacts ──────────────────────────────────────────────────────────────
    email    = models.EmailField(unique=True, null=True, blank=True, verbose_name='E-mail')
    phone    = models.CharField(max_length=50, blank=True, verbose_name='Phone')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Telegram')

    # ── Status & meta ─────────────────────────────────────────────────────────
    status = models.CharField(
        max_length=10,
        choices=PersonStatus.choices,
        default=PersonStatus.ACTIVE,
        verbose_name='Status',
    )
    notes = models.TextField(blank=True, verbose_name='Notes')
    cv    = models.FileField(
        upload_to='people/cv/',
        null=True, blank=True,
        verbose_name='CV (PDF)',
        help_text='PDF files only',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
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
