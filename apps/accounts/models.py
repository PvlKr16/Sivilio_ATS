"""
Custom User model extending Django's AbstractUser.

Extra fields added on top of the standard set:
  avatar      — profile photo (image, up to 3 MB enforced in form/admin)
  first_name  — inherited from AbstractUser (already exists)
  last_name   — inherited from AbstractUser (already exists)
  phone       — mobile / office number
  viber       — Viber contact (usually same as phone)
  telegram    — Telegram handle (@username or phone)
  role        — FK to auth.Group, single group per user
  status      — working / sleeping
  works_since — date the person joined the team
  cv          — CV file (PDF only, validated in form)
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserStatus(models.TextChoices):
    WORKING  = 'working',  'Working'
    SLEEPING = 'sleeping', 'Sleeping'


class User(AbstractUser):
    """
    Extended user model.
    Keeps all AbstractUser fields and adds HR-specific ones.
    The standard 'groups' M2M (from AbstractUser) is kept for permissions;
    'role' is a single-group FK for the business role shown in the UI.
    """

    avatar = models.ImageField(
        upload_to='users/avatars/',
        null=True,
        blank=True,
        verbose_name='Avatar',
        help_text='Profile photo, max 3 MB',
    )
    email = models.EmailField(blank=False, max_length=254, unique=True, verbose_name='email address')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Phone',)
    viber = models.CharField(max_length=100, blank=True, verbose_name='Viber', help_text='Viber number or link',)
    telegram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Telegram',
        help_text='@username or phone number',
    )
    # Single business role — FK to Django's built-in auth.Group
    role = models.ForeignKey(
        'auth.Group',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='role_users',
        verbose_name='Role',
        help_text='Business role: Superman, Supervisor, Recruiter, Client, Intern',
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.WORKING,
        verbose_name='Status',
    )
    works_since = models.DateField(
        null=True,
        blank=True,
        verbose_name='Works Since',
    )
    cv = models.FileField(
        upload_to='users/cv/',
        null=True,
        blank=True,
        verbose_name='CV (PDF)',
        help_text='Curriculum vitae, PDF format only',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        """Full name if available, otherwise username."""
        return self.get_full_name() or self.username

    @property
    def initials(self):
        """Up to 2 initials for avatar placeholder."""
        parts = [self.first_name, self.last_name]
        letters = [p[0].upper() for p in parts if p]
        if letters:
            return ''.join(letters[:2])
        return self.username[:2].upper()

    @property
    def role_name(self):
        """Return the role/group name or empty string."""
        return self.role.name if self.role else ''
