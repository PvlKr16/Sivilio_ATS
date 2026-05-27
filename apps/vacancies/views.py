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
            'company', 'level'
        ).order_by('-created_at')

        q              = self.request.GET.get('q', '').strip()
        status         = self.request.GET.get('status', '')
        company        = self.request.GET.get('company', '')
        for_freelancers = self.request.GET.get('for_freelancers', '')

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(company__name__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        if company:
            qs = qs.filter(company_id=company)
        if for_freelancers in ('0', '1'):
            qs = qs.filter(for_freelancers=bool(int(for_freelancers)))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = VacancySearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
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
