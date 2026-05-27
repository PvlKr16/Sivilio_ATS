"""
Views for the People module.
Full CRUD for Person records.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

from .models import Person
from .forms import PersonForm, PersonSearchForm


class PersonListView(LoginRequiredMixin, ListView):
    model               = Person
    template_name       = 'people/index.html'
    context_object_name = 'people'
    paginate_by         = 15

    def get_queryset(self):
        qs = Person.objects.select_related(
            'profession', 'level', 'region', 'english'
        ).order_by('last_name', 'first_name')

        q          = self.request.GET.get('q', '').strip()
        profession = self.request.GET.get('profession', '')
        level      = self.request.GET.get('level', '')
        status     = self.request.GET.get('status', '')

        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)  |
                Q(email__icontains=q)      |
                Q(phone__icontains=q)      |
                Q(telegram__icontains=q)
            )
        if profession:
            qs = qs.filter(profession_id=profession)
        if level:
            qs = qs.filter(level_id=level)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = PersonSearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
        return ctx


class PersonDetailView(LoginRequiredMixin, DetailView):
    model               = Person
    template_name       = 'people/detail.html'
    context_object_name = 'person'

    def get_queryset(self):
        return Person.objects.select_related(
            'gender', 'profession', 'level',
            'english', 'region'
        ).prefetch_related('skills', 'working_hours', 'working_place')


class PersonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model               = Person
    form_class          = PersonForm
    template_name       = 'people/form.html'
    permission_required = 'people.add_person'

    def form_valid(self, form):
        messages.success(self.request, f'Person "{form.instance.full_name}" created.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class PersonUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model               = Person
    form_class          = PersonForm
    template_name       = 'people/form.html'
    permission_required = 'people.change_person'

    def form_valid(self, form):
        messages.success(self.request, f'Person "{form.instance.full_name}" updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class PersonDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model               = Person
    template_name       = 'people/confirm_delete.html'
    success_url         = reverse_lazy('people:index')
    permission_required = 'people.delete_person'
    context_object_name = 'person'

    def form_valid(self, form):
        messages.success(self.request, 'Person deleted.')
        return super().form_valid(form)


def person_autocomplete(request):
    """JSON autocomplete endpoint for person name search."""
    q      = request.GET.get('q', '')
    people = Person.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )[:20]
    data = [{'id': p.pk, 'text': p.full_name} for p in people]
    return JsonResponse({'results': data})
