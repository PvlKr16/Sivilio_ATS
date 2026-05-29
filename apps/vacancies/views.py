"""Views for the Vacancies module."""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

from .models import Vacancy
from .forms import VacancyForm, VacancySearchForm


class VacancyListView(LoginRequiredMixin, ListView):
    model               = Vacancy
    template_name       = 'vacancies/index.html'
    context_object_name = 'vacancies'
    paginate_by         = 15

    def get_queryset(self):
        qs = Vacancy.objects.select_related(
            'company', 'level', 'english'
        ).prefetch_related(
            'supervisors', 'working_hours'
        ).order_by('-created_at')

        g = self.request.GET

        # ── Full-text search ──────────────────────────────────────────────
        q = g.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(company__name__icontains=q)
            )

        # ── Row 1 ─────────────────────────────────────────────────────────
        supervisors = g.getlist('supervisors')
        if supervisors:
            qs = qs.filter(supervisors__id__in=supervisors).distinct()

        status = g.getlist('status')
        if status:
            qs = qs.filter(status__in=status)

        company = g.getlist('company')
        if company:
            qs = qs.filter(company_id__in=company)

        # ── Row 2 ─────────────────────────────────────────────────────────
        salary_currency = g.get('salary_currency', '').strip()
        salary_from     = g.get('salary_from', '').strip()
        salary_to       = g.get('salary_to', '').strip()
        if salary_currency:
            qs = qs.filter(salary_currency=salary_currency)
        if salary_from:
            qs = qs.filter(salary_offered__gte=int(salary_from))
        if salary_to:
            qs = qs.filter(salary_offered__lte=int(salary_to))

        level = g.getlist('level')
        if level:
            qs = qs.filter(level_id__in=level)

        english = g.getlist('english')
        if english:
            qs = qs.filter(english_id__in=english)

        working_hours = g.getlist('working_hours')
        if working_hours:
            qs = qs.filter(working_hours__id__in=working_hours).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = VacancySearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()

        g = self.request.GET
        ctx['has_filters'] = any([
            g.get('q'),
            g.getlist('supervisors'), g.getlist('status'), g.getlist('company'),
            g.get('salary_currency'), g.get('salary_from'), g.get('salary_to'),
            g.getlist('level'), g.getlist('english'), g.getlist('working_hours'),
        ])
        return ctx


class VacancyDetailView(LoginRequiredMixin, DetailView):
    model               = Vacancy
    template_name       = 'vacancies/detail.html'
    context_object_name = 'vacancy'

    def get_queryset(self):
        return Vacancy.objects.select_related(
            'company', 'level', 'english'
        ).prefetch_related(
            'skills', 'working_place', 'working_hours', 'supervisors'
        )


class VacancyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model               = Vacancy
    form_class          = VacancyForm
    template_name       = 'vacancies/form.html'
    permission_required = 'vacancies.add_vacancy'

    def form_valid(self, form):
        messages.success(self.request, f'Vacancy "{form.instance.title}" created.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class VacancyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model               = Vacancy
    form_class          = VacancyForm
    template_name       = 'vacancies/form.html'
    permission_required = 'vacancies.change_vacancy'

    def form_valid(self, form):
        messages.success(self.request, f'Vacancy "{form.instance.title}" updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class VacancyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model               = Vacancy
    template_name       = 'vacancies/confirm_delete.html'
    success_url         = reverse_lazy('vacancies:index')
    permission_required = 'vacancies.delete_vacancy'
    context_object_name = 'vacancy'

    def form_valid(self, form):
        messages.success(self.request, 'Vacancy deleted.')
        return super().form_valid(form)
