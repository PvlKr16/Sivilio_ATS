"""
Models for the Companies module.
"""

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class PaymentOptions(models.TextChoices):
    FIFTY_FIFTY = '50_50',    '50/50'
    ON_FACT     = 'on_fact',  _('After')
    PREPAID     = 'prepaid',  _('Prepayment')


class CompanyStatus(models.TextChoices):
    ACTIVE   = 'active',   _('Active')
    INACTIVE = 'inactive', _('Inactive')
    LEAD     = 'lead',     _('Lead')
    PAUSED   = 'paused',   _('Paused')


class Company(models.Model):
    """Client / partner company record."""

    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Phone'))

    # Contact person — free text (name + role) or FK to Person
    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Contact Person'),
    )

    payment_options = models.CharField(
        max_length=20,
        choices=PaymentOptions.choices,
        blank=True,
        null=True,
        verbose_name=_('Payment Options'),
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Amount'),
    )
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
        verbose_name=_('Status'),
    )
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['name']
        permissions = [
            ('export_company', 'Can export company data'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        words = self.name.split()
        if len(words) >= 2:
            return f"{words[0][0]}{words[1][0]}".upper()
        return self.name[:2].upper()
