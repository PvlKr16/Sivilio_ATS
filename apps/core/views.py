"""Core views: dashboard and utility pages."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
from apps.people.models import Person, PeopleStatus
from apps.companies.models import Company


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard showing HR summary stats."""
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Summary stats for cards
        ctx['total_people'] = Person.objects.count()
        ctx['total_companies'] = Company.objects.count()
        ctx['people_no_company'] = Person.objects.filter(company__isnull=True).count()
        ctx['companies_with_vat'] = Company.objects.filter(pays_vat=True).count()

        # People by status breakdown
        ctx['status_breakdown'] = (
            PeopleStatus.objects
            .annotate(count=Count('people'))
            .filter(count__gt=0)
            .values('name', 'color', 'count')
        )

        # Recently added
        ctx['recent_people'] = (
            Person.objects
            .select_related('company', 'status')
            .order_by('-created_at')[:8]
        )
        ctx['recent_companies'] = (
            Company.objects
            .order_by('-created_at')[:6]
        )
        return ctx
