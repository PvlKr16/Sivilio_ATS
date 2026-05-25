"""
Initial migration for the companies app — simplified Company model.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True,
                                          verbose_name='Name')),
                ('email', models.EmailField(blank=True, null=True,
                                            verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=50, null=True,
                                           verbose_name='Phone')),
                ('contact_person', models.CharField(
                    blank=True, max_length=255, null=True,
                    verbose_name='Contact Person',
                )),
                ('payment_options', models.CharField(
                    blank=True, max_length=20, null=True,
                    choices=[('50_50', '50/50'), ('on_fact', 'По факту'),
                             ('prepaid', 'Предоплата')],
                    verbose_name='Payment Options',
                )),
                ('amount', models.DecimalField(
                    blank=True, null=True,
                    decimal_places=2, max_digits=12,
                    verbose_name='Amount',
                )),
                ('status', models.CharField(
                    max_length=20, default='active',
                    choices=[('active', 'Active'), ('inactive', 'Inactive'),
                             ('lead', 'Lead'), ('paused', 'Paused')],
                    verbose_name='Status',
                )),
                ('notes', models.TextField(blank=True, null=True,
                                           verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['name'],
                'permissions': [('export_company', 'Can export company data')],
            },
        ),
    ]
