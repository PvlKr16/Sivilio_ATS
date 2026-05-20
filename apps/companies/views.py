"""
Views for the Companies module.
Provides full CRUD for Company records and company-people relationships.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages

from .models import Company
from .forms import CompanyForm, CompanySearchForm


class CompanyListView(LoginRequiredMixin, ListView):
    """Paginated, filterable list of companies."""
    model = Company
    template_name = 'companies/index.html'
    context_object_name = 'companies'
    paginate_by = 15

    def get_queryset(self):
        qs = Company.objects.annotate(people_count=Count('people')).order_by('name')
        q = self.request.GET.get('q', '').strip()
        pays_vat = self.request.GET.get('pays_vat', '')
        is_tenant = self.request.GET.get('is_tenant', '')

        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(email__icontains=q)
            )
        if pays_vat in ('0', '1'):
            qs = qs.filter(pays_vat=bool(int(pays_vat)))
        if is_tenant in ('0', '1'):
            qs = qs.filter(is_tenant=bool(int(is_tenant)))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = CompanySearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
        return ctx


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """Company detail with associated people tab."""
    model = Company
    template_name = 'companies/detail.html'
    context_object_name = 'company'

    def get_queryset(self):
        return Company.objects.select_related('mandatary', 'created_by', 'updated_by')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['people'] = self.object.people.select_related('status').order_by('name')
        return ctx


class CompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a new company."""
    model = Company
    form_class = CompanyForm
    template_name = 'companies/form.html'
    permission_required = 'companies.add_company'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Company "{form.instance.name}" created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit an existing company."""
    model = Company
    form_class = CompanyForm
    template_name = 'companies/form.html'
    permission_required = 'companies.change_company'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Company "{form.instance.name}" updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class CompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a company."""
    model = Company
    template_name = 'companies/confirm_delete.html'
    success_url = reverse_lazy('companies:index')
    permission_required = 'companies.delete_company'
    context_object_name = 'company'

    def form_valid(self, form):
        messages.success(self.request, 'Company deleted successfully.')
        return super().form_valid(form)
