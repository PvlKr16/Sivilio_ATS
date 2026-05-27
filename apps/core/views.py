"""Core views: dashboard."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count

from apps.people.models import Person, PersonStatus
from apps.companies.models import Company
from apps.vacancies.models import Vacancy


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard showing HR summary stats."""
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Summary stat cards
        ctx['total_people']    = Person.objects.count()
        ctx['total_companies'] = Company.objects.count()
        ctx['active_people']   = Person.objects.filter(status=PersonStatus.ACTIVE).count()
        ctx['total_vacancies'] = Vacancy.objects.count()

        # People by status breakdown
        ctx['status_breakdown'] = (
            Person.objects
            .values('status')
            .annotate(count=Count('status'))
            .filter(count__gt=0)
            .order_by('status')
        )

        # Recently added people
        ctx['recent_people'] = (
            Person.objects
            .select_related('level')
            .order_by('-created_at')[:8]
        )

        # Recently added companies
        ctx['recent_companies'] = (
            Company.objects
            .order_by('-created_at')[:6]
        )

        # Recently added vacancies
        ctx['recent_vacancies'] = (
            Vacancy.objects
            .order_by('-created_at')[:6]
        )

        return ctx
