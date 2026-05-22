"""
Initial migration for the companies app.
Company no longer has a mandatary FK to Person (simplified).
"""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Company Name')),
                ('email', models.EmailField(blank=True, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone')),
                ('fax', models.CharField(blank=True, max_length=50, null=True, verbose_name='Fax')),
                ('bank', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bank')),
                ('bank_account', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bank Account')),
                ('pays_vat', models.BooleanField(default=False, verbose_name='Pays VAT')),
                ('is_tenant', models.BooleanField(default=False, verbose_name='Is Tenant')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observations')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='companies/logos/', verbose_name='Logo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mandatary', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='mandatary_of',
                    to='people.person',
                    verbose_name='Mandatary',
                )),
                ('created_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='companies_created',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Created By',
                )),
                ('updated_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='companies_updated',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Updated By',
                )),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['name'],
                'permissions': [('export_company', 'Can export company data')],
            },
        ),
    ]
