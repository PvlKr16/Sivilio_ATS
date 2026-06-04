"""
Models for the Events module.
Tracks recruitment pipeline events for candidates.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class EventType(models.TextChoices):
    CANDIDATE_PROCESSED = 'candidate_processed', _('Candidate processed')
    CV_REVIEW           = 'cv_review',           _('CV review')
    PHONE_INTERVIEW     = 'phone_interview',      _('Phone interview')
    INTERVIEW           = 'interview',            _('Interview')
    TEST_ASSIGNMENT     = 'test_assignment',      _('Test assignment')
    OFFER               = 'offer',                _('Offer')


# Badge colour mapped to each event type — used in templates
EVENT_TYPE_BADGE = {
    'candidate_processed': 'secondary',
    'cv_review':           'info',
    'phone_interview':     'primary',
    'interview':           'warning',
    'test_assignment':     'primary',
    'offer':               'success',
}


class Event(models.Model):
    """A recruitment pipeline event linking a candidate, vacancy and company."""

    event_type = models.CharField(
        max_length=30,
        choices=EventType.choices,
        verbose_name=_('Event Type'),
    )
    vacancy = models.ForeignKey(
        'vacancies.Vacancy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        verbose_name=_('Vacancy'),
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        verbose_name=_('Company'),
    )
    candidate = models.ForeignKey(
        'people.Person',
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name=_('Candidate'),
    )
    event_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Event Date'),
    )
    event_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name=_('Event Time'),
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_events',
        limit_choices_to={'role__name': 'Supervisor'},
        verbose_name=_('Supervisor'),
    )
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-event_date', '-event_time', '-created_at']

    def __str__(self):
        return f"{self.get_event_type_display()} — {self.candidate}"

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    @property
    def badge_color(self):
        """Return bootstrap-style badge colour for this event type."""
        return EVENT_TYPE_BADGE.get(self.event_type, 'secondary')

    @property
    def datetime_display(self):
        """Human-readable date + time."""
        parts = []
        if self.event_date:
            parts.append(self.event_date.strftime('%d %b %Y'))
        if self.event_time:
            parts.append(self.event_time.strftime('%H:%M'))
        return ' '.join(parts) if parts else '—'
