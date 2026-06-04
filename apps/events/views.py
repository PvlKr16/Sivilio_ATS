"""Views for the Events module."""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Event
from .forms import EventForm, EventSearchForm


class EventListView(LoginRequiredMixin, ListView):
    model               = Event
    template_name       = 'events/index.html'
    context_object_name = 'events'
    paginate_by         = 20

    def get_queryset(self):
        qs = Event.objects.select_related(
            'candidate', 'vacancy', 'company', 'supervisor'
        ).order_by('-event_date', '-event_time', '-created_at')

        q           = self.request.GET.get('q', '').strip()
        event_types = self.request.GET.getlist('event_type')
        companies   = self.request.GET.getlist('company')
        supervisors = self.request.GET.getlist('supervisor')
        vacancies   = self.request.GET.getlist('vacancy')
        candidates  = self.request.GET.getlist('candidate')
        date_from   = self.request.GET.get('date_from', '').strip()
        date_to     = self.request.GET.get('date_to', '').strip()

        if q:
            qs = qs.filter(
                Q(candidate__first_name__icontains=q) |
                Q(candidate__last_name__icontains=q)  |
                Q(vacancy__title__icontains=q)         |
                Q(notes__icontains=q)
            )
        if event_types:
            qs = qs.filter(event_type__in=event_types)
        if companies:
            qs = qs.filter(company_id__in=companies)
        if supervisors:
            qs = qs.filter(supervisor_id__in=supervisors)
        if vacancies:
            qs = qs.filter(vacancy_id__in=vacancies)
        if candidates:
            qs = qs.filter(candidate_id__in=candidates)
        if date_from:
            qs = qs.filter(event_date__gte=date_from)
        if date_to:
            qs = qs.filter(event_date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = EventSearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
        ctx['has_filters'] = bool(
            self.request.GET.get('q')                    or
            self.request.GET.getlist('event_type')       or
            self.request.GET.getlist('company')          or
            self.request.GET.getlist('supervisor')       or
            self.request.GET.getlist('vacancy')          or
            self.request.GET.getlist('candidate')        or
            self.request.GET.get('date_from')            or
            self.request.GET.get('date_to')
        )
        return ctx


class EventDetailView(LoginRequiredMixin, DetailView):
    model               = Event
    template_name       = 'events/detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        return Event.objects.select_related(
            'candidate', 'vacancy', 'company', 'supervisor'
        )


class EventCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model               = Event
    form_class          = EventForm
    template_name       = 'events/form.html'
    permission_required = 'events.add_event'

    def get_initial(self):
        """Pre-fill candidate / vacancy / company from query params."""
        initial = super().get_initial()
        for key in ('candidate', 'vacancy', 'company'):
            val = self.request.GET.get(key)
            if val:
                initial[key] = val
        return initial

    def form_valid(self, form):
        messages.success(self.request, _('Event "%(title)s" created.') %{'title':form.instance.get_event_type_display()},)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = _('Create')
        return ctx


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model               = Event
    form_class          = EventForm
    template_name       = 'events/form.html'
    permission_required = 'events.change_event'

    def form_valid(self, form):
        messages.success(self.request, _('Event "%(title)s" updated.') %{'title':form.instance.get_event_type_display()},)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = _('Edit')
        return ctx


class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model               = Event
    template_name       = 'events/confirm_delete.html'
    success_url         = reverse_lazy('events:index')
    permission_required = 'events.delete_event'
    context_object_name = 'event'

    def form_valid(self, form):
        messages.success(self.request, _('Event deleted.'))
        return super().form_valid(form)
