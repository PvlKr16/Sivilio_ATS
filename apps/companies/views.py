"""Views for the Companies module."""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Company
from .forms import CompanyForm, CompanySearchForm


class CompanyListView(LoginRequiredMixin, ListView):
    model               = Company
    template_name       = 'companies/index.html'
    context_object_name = 'companies'
    paginate_by         = 15

    def get_queryset(self):
        qs = Company.objects.order_by('name')
        q               = self.request.GET.get('q', '').strip()
        statuses        = self.request.GET.getlist('status')
        payment_options = self.request.GET.getlist('payment_options')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
        if statuses:
            qs = qs.filter(status__in=statuses)
        if payment_options:
            qs = qs.filter(payment_options__in=payment_options)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = CompanySearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
        ctx['has_filters'] = bool(
            self.request.GET.get('q') or
            self.request.GET.getlist('status') or
            self.request.GET.getlist('payment_options')
        )
        return ctx


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/detail.html'
    context_object_name = 'company'

    def get_queryset(self):
        return Company.objects.all()


class CompanyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model               = Company
    form_class          = CompanyForm
    template_name       = 'companies/form.html'
    permission_required = 'companies.add_company'

    def form_valid(self, form):
        messages.success(self.request, _('Company "%(title)s" created.') % {'title': form.instance.name})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = _('Create')
        return ctx


class CompanyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model               = Company
    form_class          = CompanyForm
    template_name       = 'companies/form.html'
    permission_required = 'companies.change_company'

    def form_valid(self, form):
        messages.success(self.request, _('Company "%(title)s" updated.') % {'title': form.instance.name})
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = _('Edit')
        return ctx


class CompanyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model               = Company
    template_name       = 'companies/confirm_delete.html'
    success_url         = reverse_lazy('companies:index')
    permission_required = 'companies.delete_company'
    context_object_name = 'company'

    def form_valid(self, form):
        messages.success(self.request, _('Company deleted.'))
        return super().form_valid(form)