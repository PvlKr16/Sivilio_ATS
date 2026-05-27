"""
Models for the Vacancies module.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse


class VacancyStatus(models.TextChoices):
    IN_PROGRESS = 'in_progress', 'В работе'
    STOP        = 'stop',        'Стоп'


class CurrencyChoices(models.TextChoices):
    USD = 'USD', 'USD ($)'
    EUR = 'EUR', 'EUR (€)'
    UAH = 'UAH', 'UAH (₴)'
    RUB = 'RUB', 'RUB (₽)'
    GBP = 'GBP', 'GBP (£)'


class Vacancy(models.Model):
    """Job vacancy / open position."""

    status = models.CharField(
        max_length=20,
        choices=VacancyStatus.choices,
        default=VacancyStatus.IN_PROGRESS,
        verbose_name='Status',
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Company',
    )
    title = models.CharField(max_length=255, verbose_name='Title')

    # Skills — shared with Person
    skills = models.ManyToManyField(
        'people.Skill',
        blank=True,
        related_name='vacancies',
        verbose_name='Skills Required',
    )

    # Salary
    salary_offered = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Salary Offered',
    )
    salary_currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD,
        blank=True,
        verbose_name='Currency',
    )

    # Reference fields — shared with Person
    level = models.ForeignKey(
        'people.Level',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Level',
    )
    english = models.ForeignKey(
        'people.English',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='English',
    )
    working_place = models.ManyToManyField(
        'people.WorkingPlace',
        blank=True,
        verbose_name='Working Place',
    )
    working_hours = models.ManyToManyField(
        'people.WorkingHours',
        blank=True,
        verbose_name='Working Hours',
    )

    screening = models.TextField(
        blank=True,
        verbose_name='Screening',
        help_text='Interview questions, screening criteria, notes',
    )
    for_freelancers = models.BooleanField(
        default=False,
        verbose_name='For Freelancers',
    )

    # Supervisors — only Users whose role.name == 'Supervisor'
    supervisors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='supervised_vacancies',
        verbose_name='Supervisors',
        limit_choices_to={'role__name': 'Supervisor'},
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
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
