"""
Models for the People module.
Mirrors the Laravel Enso people package schema.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse


class TitleChoices(models.IntegerChoices):
    """Salutation titles matching the original tinyInteger field."""
    MR = 1, 'Mr'
    MRS = 2, 'Mrs'
    MS = 3, 'Ms'
    DR = 4, 'Dr'
    PROF = 5, 'Prof'


class GenderChoices(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class PeopleStatus(models.Model):
    """Employment/engagement status for a person."""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, default='secondary')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'People Status'
        verbose_name_plural = 'People Statuses'
        ordering = ['name']

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    """Education level reference (mirrors enso Level model)."""
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Education Level'
        verbose_name_plural = 'Education Levels'
        ordering = ['order']

    def __str__(self):
        return self.name


class Person(models.Model):
    """
    Core person entity.
    Mirrors the 'people' table from the original Laravel migration.
    """

    # Optional link to a company (added in create_companies_table migration)
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='people',
        verbose_name='Company',
    )

    title = models.PositiveSmallIntegerField(
        choices=TitleChoices.choices,
        null=True,
        blank=True,
        verbose_name='Title',
    )
    name = models.CharField(max_length=255, verbose_name='Full Name')
    appellative = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Appellative',
        help_text='Preferred way to address this person',
    )

    # Unique identifiers
    uid = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name='UID',
        help_text='Tax ID / National ID',
    )
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='Email')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Phone')
    birthday = models.DateField(null=True, blank=True, verbose_name='Birthday')

    # Job position (free-text, not FK - matches original schema)
    position = models.CharField(max_length=255, blank=True, null=True, verbose_name='Position')

    # HR status
    status = models.ForeignKey(
        PeopleStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='people',
        verbose_name='Status',
    )

    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        blank=True,
        null=True,
        verbose_name='Gender',
    )

    obs = models.TextField(blank=True, null=True, verbose_name='Observations')

    # Avatar / photo
    avatar = models.ImageField(
        upload_to='people/avatars/',
        null=True,
        blank=True,
        verbose_name='Photo',
    )

    # Audit fields (mirrors created_by / updated_by FK pattern)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='people_created',
        verbose_name='Created By',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='people_updated',
        verbose_name='Updated By',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name']
        permissions = [
            ('export_person', 'Can export people data'),
        ]

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('people:detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        """Return title + name."""
        if self.title:
            return f"{self.get_title_display()} {self.name}"
        return self.name

    @property
    def initials(self):
        """Return up to 2 initials for avatar placeholder."""
        parts = self.name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return self.name[:2].upper()


class Education(models.Model):
    """Education record for a person (mirrors enso Education model)."""

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='educations',
        verbose_name='Person',
    )
    level = models.ForeignKey(
        EducationLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Level',
    )
    institution = models.CharField(max_length=255, verbose_name='Institution')
    specialization = models.CharField(max_length=255, blank=True, verbose_name='Specialization')
    year_start = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Year Start')
    year_end = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Year End')
    notes = models.TextField(blank=True, verbose_name='Notes')

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Education Records'
        ordering = ['-year_end', '-year_start']

    def __str__(self):
        return f"{self.person.name} — {self.institution}"


class Work(models.Model):
    """Work experience record for a person (mirrors enso Work model)."""

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='works',
        verbose_name='Person',
    )
    employer = models.CharField(max_length=255, verbose_name='Employer')
    position = models.CharField(max_length=255, blank=True, verbose_name='Position')
    date_start = models.DateField(null=True, blank=True, verbose_name='Start Date')
    date_end = models.DateField(null=True, blank=True, verbose_name='End Date')
    is_current = models.BooleanField(default=False, verbose_name='Current Job')
    notes = models.TextField(blank=True, verbose_name='Notes')

    class Meta:
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experience'
        ordering = ['-date_start']

    def __str__(self):
        return f"{self.person.name} @ {self.employer}"
