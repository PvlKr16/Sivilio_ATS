"""
Custom User model extending Django's AbstractUser.
Links users to Person records for HR functionality.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model linked to a Person record."""

    person = models.OneToOneField(
        'people.Person',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user',
        verbose_name='Person',
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        """Return person name if linked, otherwise username."""
        if self.person:
            return self.person.full_name
        return self.get_full_name() or self.username
