"""
Management command: create_initial_data
Runs on first deploy (see docker-compose.yml).
Seeds: auth Groups (roles), PeopleStatus, EducationLevel, superuser.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial reference data and create the default superuser'

    def handle(self, *args, **options):
        self._create_groups()
        self._create_statuses()
        self._create_education_levels()
        self._create_superuser()
        self.stdout.write(self.style.SUCCESS('Initial data ready.'))

    # ── Groups (business roles) ───────────────────────────────────────────
    def _create_groups(self):
        """Load the five role groups from the fixture."""
        call_command('loaddata', 'groups', verbosity=0)
        self.stdout.write('  Groups: OK')

    # ── People statuses ───────────────────────────────────────────────────
    def _create_statuses(self):
        from apps.people.models import PeopleStatus
        data = [
            ('Active',     'success'),
            ('On Leave',   'warning'),
            ('Contractor', 'info'),
            ('Inactive',   'secondary'),
            ('Candidate',  'primary'),
        ]
        for name, color in data:
            PeopleStatus.objects.get_or_create(name=name, defaults={'color': color})
        self.stdout.write('  People statuses: OK')

    # ── Education levels ──────────────────────────────────────────────────
    def _create_education_levels(self):
        from apps.people.models import EducationLevel
        data = [
            ('Secondary',  1),
            ('Vocational', 2),
            ('Bachelor',   3),
            ('Master',     4),
            ('PhD',        5),
            ('MBA',        6),
        ]
        for name, order in data:
            EducationLevel.objects.get_or_create(name=name, defaults={'order': order})
        self.stdout.write('  Education levels: OK')

    # ── Default superuser ─────────────────────────────────────────────────
    def _create_superuser(self):
        if not User.objects.filter(is_superuser=True).exists():
            from django.contrib.auth.models import Group
            superman = Group.objects.filter(name='Superman').first()
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role=superman,
                status='working',
            )
            self.stdout.write(
                self.style.WARNING(
                    '  Superuser created: admin / admin123  ← CHANGE THIS PASSWORD!'
                )
            )
        else:
            self.stdout.write('  Superuser: already exists')
