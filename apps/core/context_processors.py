"""
Template context processors.
Inject navigation counts into every template.
"""

from apps.people.models import Person
from apps.companies.models import Company


def sidebar_context(request):
    """Provide counts and nav state for the sidebar on every page."""
    if not request.user.is_authenticated:
        return {}

    # Import here to avoid circular imports at startup
    from apps.vacancies.models import Vacancy

    return {
        'nav_people_count':    Person.objects.count(),
        'nav_companies_count': Company.objects.count(),
        'nav_vacancies_count': Vacancy.objects.filter(status='in_progress').count(),
        'current_path':        request.path,
    }
