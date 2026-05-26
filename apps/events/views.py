"""Views for the Events module."""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages

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

        q          = self.request.GET.get('q', '').strip()
        event_type = self.request.GET.get('event_type', '')
        company    = self.request.GET.get('company', '')
        supervisor = self.request.GET.get('supervisor', '')

        if q:
            qs = qs.filter(
                Q(candidate__first_name__icontains=q) |
                Q(candidate__last_name__icontains=q)  |
                Q(vacancy__title__icontains=q)         |
                Q(notes__icontains=q)
            )
        if event_type:
            qs = qs.filter(event_type=event_type)
        if company:
            qs = qs.filter(company_id=company)
        if supervisor:
            qs = qs.filter(supervisor_id=supervisor)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = EventSearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
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
        messages.success(self.request,
                         f'Event "{form.instance.get_event_type_display()}" created.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class EventUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model               = Event
    form_class          = EventForm
    template_name       = 'events/form.html'
    permission_required = 'events.change_event'

    def form_valid(self, form):
        messages.success(self.request,
                         f'Event "{form.instance.get_event_type_display()}" updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class EventDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model               = Event
    template_name       = 'events/confirm_delete.html'
    success_url         = reverse_lazy('events:index')
    permission_required = 'events.delete_event'
    context_object_name = 'event'

    def form_valid(self, form):
        messages.success(self.request, 'Event deleted.')
        return super().form_valid(form)
