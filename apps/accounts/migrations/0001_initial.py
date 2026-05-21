"""
Initial migration for the accounts app.
Creates the custom User table with all HR fields.
Does NOT reference people.Person to avoid circular deps —
that FK lives in people.0001_initial.
"""

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True,
                                                    verbose_name='last login')),
                ('is_superuser', models.BooleanField(
                    default=False,
                    help_text='Designates that this user has all permissions without '
                              'explicitly assigning them.',
                    verbose_name='superuser status',
                )),
                ('username', models.CharField(
                    error_messages={'unique': 'A user with that username already exists.'},
                    help_text='Required. 150 characters or fewer. '
                              'Letters, digits and @/./+/-/_ only.',
                    max_length=150, unique=True,
                    validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                    verbose_name='username',
                )),
                ('first_name', models.CharField(blank=True, max_length=150,
                                                verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150,
                                               verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254,
                                            verbose_name='email address')),
                ('is_staff', models.BooleanField(
                    default=False,
                    help_text='Designates whether the user can log into this admin site.',
                    verbose_name='staff status',
                )),
                ('is_active', models.BooleanField(
                    default=True,
                    help_text='Designates whether this user should be treated as active.',
                    verbose_name='active',
                )),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now,
                                                     verbose_name='date joined')),
                # ── HR-specific fields ──────────────────────────────────────
                ('avatar', models.ImageField(
                    blank=True, null=True,
                    upload_to='users/avatars/',
                    verbose_name='Avatar',
                    help_text='Profile photo, max 3 MB',
                )),
                ('phone', models.CharField(blank=True, max_length=50,
                                           verbose_name='Phone')),
                ('viber', models.CharField(blank=True, max_length=100,
                                           verbose_name='Viber',
                                           help_text='Viber number or link')),
                ('telegram', models.CharField(blank=True, max_length=100,
                                              verbose_name='Telegram',
                                              help_text='@username or phone number')),
                ('role', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='role_users',
                    to='auth.group',
                    verbose_name='Role',
                    help_text='Business role: Superman, Supervisor, Recruiter, Client, Intern',
                )),
                ('status', models.CharField(
                    max_length=20,
                    choices=[('working', 'Working'), ('sleeping', 'Sleeping')],
                    default='working',
                    verbose_name='Status',
                )),
                ('works_since', models.DateField(blank=True, null=True,
                                                 verbose_name='Works Since')),
                ('cv', models.FileField(
                    blank=True, null=True,
                    upload_to='users/cv/',
                    verbose_name='CV (PDF)',
                    help_text='Curriculum vitae, PDF format only',
                )),
                # ── Standard M2M from AbstractUser ──────────────────────────
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text='The groups this user belongs to.',
                    related_name='user_set', related_query_name='user',
                    to='auth.group', verbose_name='groups',
                )),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    help_text='Specific permissions for this user.',
                    related_name='user_set', related_query_name='user',
                    to='auth.permission', verbose_name='user permissions',
                )),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
