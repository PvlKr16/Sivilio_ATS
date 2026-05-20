"""
Models for the Companies module.
Mirrors the 2018_10_07_100000_create_companies_table.php migration.
"""

from django.db import models
from django.conf import settings
from django.urls import reverse


class Company(models.Model):
    """
    Company entity.
    Mirrors the 'companies' table from the original Laravel migration.
    """

    # Mandatary — the person legally representing the company
    mandatary = models.ForeignKey(
        'people.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mandatary_of',
        verbose_name='Mandatary',
        help_text='Legal representative of the company',
    )

    name = models.CharField(max_length=255, unique=True, verbose_name='Company Name')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Phone')
    fax = models.CharField(max_length=50, blank=True, null=True, verbose_name='Fax')

    # Banking details
    bank = models.CharField(max_length=255, blank=True, null=True, verbose_name='Bank')
    bank_account = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bank Account')

    # Flags (stored as boolean, original used string 'boolean' which was a quirk)
    pays_vat = models.BooleanField(default=False, verbose_name='Pays VAT')
    is_tenant = models.BooleanField(default=False, verbose_name='Is Tenant')

    obs = models.TextField(blank=True, null=True, verbose_name='Observations')

    # Logo image
    logo = models.ImageField(
        upload_to='companies/logos/',
        null=True,
        blank=True,
        verbose_name='Logo',
    )

    # Audit fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies_created',
        verbose_name='Created By',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies_updated',
        verbose_name='Updated By',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
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
        """Return up to 2 initials for logo placeholder."""
        words = self.name.split()
        if len(words) >= 2:
            return f"{words[0][0]}{words[1][0]}".upper()
        return self.name[:2].upper()

    @property
    def people_count(self):
        return self.people.count()
