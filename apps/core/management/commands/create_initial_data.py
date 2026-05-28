"""
Management command: create_initial_data
Seeds: auth Groups, People reference data, Skills, superuser.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial reference data and create the default superuser'

    def handle(self, *args, **options):
        self._create_groups()
        self._create_people_reference_data()
        self._create_skills()
        self._create_superuser()
        self._create_users()
        self._create_companies()
        self._create_people()
        self._create_vacancies()
        self.stdout.write(self.style.SUCCESS('Initial data ready.'))

    def _create_groups(self):
        call_command('loaddata', 'groups', verbosity=0)
        self.stdout.write('  Groups: OK')

    def _create_people_reference_data(self):
        call_command('loaddata', 'reference_data', verbosity=0)
        self.stdout.write('  People reference data: OK')

    def _create_skills(self):
        call_command('loaddata', 'skills', verbosity=0)
        self.stdout.write('  Skills: OK')

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
                    '  Superuser created: admin / admin123  <- CHANGE THIS PASSWORD!'
                )
            )
        else:
            self.stdout.write('  Superuser: already exists')

    def _create_users(self):
        call_command('loaddata', 'users', verbosity=0)
        self.stdout.write('  Users: OK')

    def _create_companies(self):
        call_command('loaddata', 'companies', verbosity=0)
        self.stdout.write('  Companies: OK')

    def _create_people(self):
        call_command('loaddata', 'people', verbosity=0)
        self.stdout.write('  People: OK')

    def _create_vacancies(self):
        call_command('loaddata', 'vacancies', verbosity=0)
        self.stdout.write('  Vacancies: OK')
