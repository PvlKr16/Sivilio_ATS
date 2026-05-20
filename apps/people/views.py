"""
Views for the People module.
Provides CRUD for Person records plus nested Education and Work records.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Person, Education, Work
from .forms import PersonForm, PersonSearchForm, EducationForm, WorkForm


class PersonListView(LoginRequiredMixin, ListView):
    """Paginated, filterable list of all people."""
    model = Person
    template_name = 'people/index.html'
    context_object_name = 'people'
    paginate_by = 15

    def get_queryset(self):
        qs = Person.objects.select_related('company', 'status').order_by('name')
        q = self.request.GET.get('q', '').strip()
        company = self.request.GET.get('company', '')
        status = self.request.GET.get('status', '')

        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(email__icontains=q) |
                Q(position__icontains=q) |
                Q(uid__icontains=q)
            )
        if company:
            qs = qs.filter(company_id=company)
        if status:
            qs = qs.filter(status_id=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = PersonSearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()
        return ctx


class PersonDetailView(LoginRequiredMixin, DetailView):
    """Person detail page with education and work tabs."""
    model = Person
    template_name = 'people/detail.html'
    context_object_name = 'person'

    def get_queryset(self):
        return Person.objects.select_related('company', 'status', 'created_by', 'updated_by')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['educations'] = self.object.educations.select_related('level').all()
        ctx['works'] = self.object.works.all()
        ctx['education_form'] = EducationForm()
        ctx['work_form'] = WorkForm()
        return ctx


class PersonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a new person record."""
    model = Person
    form_class = PersonForm
    template_name = 'people/form.html'
    permission_required = 'people.add_person'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Person "{form.instance.name}" created successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class PersonUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit an existing person record."""
    model = Person
    form_class = PersonForm
    template_name = 'people/form.html'
    permission_required = 'people.change_person'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Person "{form.instance.name}" updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class PersonDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a person record."""
    model = Person
    template_name = 'people/confirm_delete.html'
    success_url = reverse_lazy('people:index')
    permission_required = 'people.delete_person'
    context_object_name = 'person'

    def form_valid(self, form):
        messages.success(self.request, 'Person deleted successfully.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Education nested views (AJAX-friendly)
# ---------------------------------------------------------------------------

class EducationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Add an education record to a person."""
    model = Education
    form_class = EducationForm
    permission_required = 'people.add_education'

    def form_valid(self, form):
        person = get_object_or_404(Person, pk=self.kwargs['person_pk'])
        form.instance.person = person
        form.save()
        messages.success(self.request, 'Education record added.')
        return redirect('people:detail', pk=person.pk)

    def form_invalid(self, form):
        person = get_object_or_404(Person, pk=self.kwargs['person_pk'])
        messages.error(self.request, 'Please correct the errors below.')
        return redirect('people:detail', pk=person.pk)


class EducationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Remove an education record."""
    model = Education
    permission_required = 'people.delete_education'

    def get_success_url(self):
        return reverse_lazy('people:detail', kwargs={'pk': self.object.person_id})

    def form_valid(self, form):
        messages.success(self.request, 'Education record removed.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Work Experience nested views
# ---------------------------------------------------------------------------

class WorkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Add a work experience record to a person."""
    model = Work
    form_class = WorkForm
    permission_required = 'people.add_work'

    def form_valid(self, form):
        person = get_object_or_404(Person, pk=self.kwargs['person_pk'])
        form.instance.person = person
        form.save()
        messages.success(self.request, 'Work experience added.')
        return redirect('people:detail', pk=person.pk)

    def form_invalid(self, form):
        person = get_object_or_404(Person, pk=self.kwargs['person_pk'])
        messages.error(self.request, 'Please correct the errors below.')
        return redirect('people:detail', pk=person.pk)


class WorkDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Remove a work experience record."""
    model = Work
    permission_required = 'people.delete_work'

    def get_success_url(self):
        return reverse_lazy('people:detail', kwargs={'pk': self.object.person_id})

    def form_valid(self, form):
        messages.success(self.request, 'Work record removed.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# AJAX autocomplete endpoint
# ---------------------------------------------------------------------------

def person_autocomplete(request):
    """Return JSON list of people matching the query (for select2 / autocomplete)."""
    q = request.GET.get('q', '')
    people = Person.objects.filter(
        Q(name__icontains=q) | Q(email__icontains=q)
    )[:20]
    data = [{'id': p.pk, 'text': str(p)} for p in people]
    return JsonResponse({'results': data})
