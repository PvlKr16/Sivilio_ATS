"""
Template context processors.
Inject navigation and summary data into every template.
"""

from apps.people.models import Person
from apps.companies.models import Company


def sidebar_context(request):
    """Provide counts and nav state for the sidebar on every page."""
    if not request.user.is_authenticated:
        return {}

    return {
        'nav_people_count': Person.objects.count(),
        'nav_companies_count': Company.objects.count(),
        'current_path': request.path,
    }
