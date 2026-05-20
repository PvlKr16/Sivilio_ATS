"""
Core application utilities:
- Dashboard view
- Audit middleware (sets created_by / updated_by)
- Context processors for sidebar nav
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    label = 'core'
    verbose_name = 'Core'
