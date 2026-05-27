"""Initial migration for the Vacancies app."""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
        ('people',    '0001_initial'),
        (settings.AUTH_USER_MODEL.split('.')[0], '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    max_length=20, default='in_progress',
                    choices=[('in_progress', 'В работе'), ('stop', 'Стоп')],
                    verbose_name='Status',
                )),
                ('company', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='vacancies',
                    to='companies.company',
                    verbose_name='Company',
                )),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('skills', models.ManyToManyField(
                    blank=True,
                    related_name='vacancies',
                    to='people.skill',
                    verbose_name='Skills Required',
                )),
                ('salary_offered', models.DecimalField(
                    blank=True, null=True,
                    decimal_places=2, max_digits=10,
                    verbose_name='Salary Offered',
                )),
                ('salary_currency', models.CharField(
                    blank=True, max_length=3, default='USD',
                    choices=[('USD','USD ($)'),('EUR','EUR (€)'),
                             ('UAH','UAH (₴)'),('RUB','RUB (₽)'),('GBP','GBP (£)')],
                    verbose_name='Currency',
                )),
                ('level', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='people.level',
                    verbose_name='Level',
                )),
                ('english', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='people.english',
                    verbose_name='English',
                )),
                ('working_place', models.ManyToManyField(
                    blank=True,
                    to='people.workingplace',
                    verbose_name='Working Place',
                )),
                ('working_hours', models.ManyToManyField(
                    blank=True,
                    to='people.workinghours',
                    verbose_name='Working Hours',
                )),
                ('screening', models.TextField(blank=True, verbose_name='Screening')),
                ('for_freelancers', models.BooleanField(
                    default=False, verbose_name='For Freelancers',
                )),
                ('supervisors', models.ManyToManyField(
                    blank=True,
                    related_name='supervised_vacancies',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Supervisors',
                    limit_choices_to={'role__name': 'Supervisor'},
                )),
                ('created_at', models.DateTimeField(auto_now_add=True,
                                                    verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vacancies',
                'ordering': ['-created_at'],
            },
        ),
    ]
