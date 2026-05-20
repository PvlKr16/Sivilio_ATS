"""
Management command: create_initial_data
Seeds the database with default statuses, education levels, and a superuser.
Run automatically on first deploy via docker-compose command.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create initial reference data (statuses, levels, superuser)'

    def handle(self, *args, **options):
        self._create_statuses()
        self._create_education_levels()
        self._create_superuser()
        self.stdout.write(self.style.SUCCESS('Initial data created successfully.'))

    def _create_statuses(self):
        """Seed PeopleStatus reference data."""
        from apps.people.models import PeopleStatus
        statuses = [
            ('Active', 'success'),
            ('On Leave', 'warning'),
            ('Contractor', 'info'),
            ('Inactive', 'secondary'),
            ('Candidate', 'primary'),
        ]
        for name, color in statuses:
            PeopleStatus.objects.get_or_create(name=name, defaults={'color': color})
        self.stdout.write('  People statuses: OK')

    def _create_education_levels(self):
        """Seed EducationLevel reference data."""
        from apps.people.models import EducationLevel
        levels = [
            ('Secondary', 1),
            ('Vocational', 2),
            ('Bachelor', 3),
            ('Master', 4),
            ('PhD', 5),
            ('MBA', 6),
        ]
        for name, order in levels:
            EducationLevel.objects.get_or_create(name=name, defaults={'order': order})
        self.stdout.write('  Education levels: OK')

    def _create_superuser(self):
        """Create default admin if no superuser exists."""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
            )
            self.stdout.write(
                self.style.WARNING('  Superuser created: admin / admin123 — CHANGE PASSWORD!')
            )
        else:
            self.stdout.write('  Superuser: already exists')
