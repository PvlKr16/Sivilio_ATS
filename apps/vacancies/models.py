"""
Models for the Vacancies module.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ..core.choices import CurrencyChoices


class VacancyStatus(models.TextChoices):
    IN_PROGRESS = 'in_progress', _('In Progress')
    STOP        = 'stop',        _('Stop')


class Vacancy(models.Model):
    """Job vacancy / open position."""

    status = models.CharField(
        max_length=20,
        choices=VacancyStatus.choices,
        default=VacancyStatus.IN_PROGRESS,
        verbose_name=_('Status'),
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name=_('Company'),
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))

    skills = models.ManyToManyField(
        'people.Skill',
        blank=True,
        related_name='vacancies',
        verbose_name=_('Skills Required'),
    )

    salary_offered = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Salary Offered'),
    )
    salary_currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
        blank=True,
        verbose_name=_('Currency'),
    )

    level = models.ForeignKey(
        'people.Level',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Level'),
    )
    english = models.ForeignKey(
        'people.English',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('English'),
    )
    working_place = models.ManyToManyField(
        'people.WorkingPlace',
        blank=True,
        verbose_name=_('Working Place'),
    )
    working_hours = models.ManyToManyField(
        'people.WorkingHours',
        blank=True,
        verbose_name=_('Working Hours'),
    )

    screening = models.TextField(
        blank=True,
        verbose_name=_('Screening'),
        help_text=_('Interview questions, screening criteria, notes'),
    )
    for_freelancers = models.BooleanField(
        default=False,
        verbose_name=_('For Freelancers'),
    )

    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='supervised_vacancies',
        verbose_name=_('Supervisors'),
        limit_choices_to={'role__name': 'Supervisor'},
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Vacancy')
        verbose_name_plural = _('Vacancies')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.company}"

    def get_absolute_url(self):
        return reverse('vacancies:detail', kwargs={'pk': self.pk})

    @property
    def salary_display(self):
        if self.salary_offered:
            return f"{self.salary_offered:,.0f} {self.salary_currency}"
        return '—'
