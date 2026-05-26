"""Initial migration for the Events app."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people',    '0001_initial'),
        ('companies', '0001_initial'),
        ('vacancies', '0001_initial'),
        (settings.AUTH_USER_MODEL.split('.')[0], '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(
                    max_length=30,
                    choices=[
                        ('candidate_processed', 'Candidate processed'),
                        ('cv_review',           'CV review'),
                        ('phone_interview',     'Phone interview'),
                        ('interview',           'Interview'),
                        ('test_assignment',     'Test assignment'),
                        ('offer',               'Offer'),
                    ],
                    verbose_name='Event Type',
                )),
                ('vacancy', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='events',
                    to='vacancies.vacancy',
                    verbose_name='Vacancy',
                )),
                ('company', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='events',
                    to='companies.company',
                    verbose_name='Company',
                )),
                ('candidate', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='events',
                    to='people.person',
                    verbose_name='Candidate',
                )),
                ('event_date', models.DateField(
                    blank=True, null=True, verbose_name='Event Date',
                )),
                ('event_time', models.TimeField(
                    blank=True, null=True, verbose_name='Event Time',
                )),
                ('supervisor', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='supervised_events',
                    limit_choices_to={'role__name': 'Supervisor'},
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Supervisor',
                )),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, verbose_name='Created At',
                )),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['-event_date', '-event_time', '-created_at'],
            },
        ),
    ]
