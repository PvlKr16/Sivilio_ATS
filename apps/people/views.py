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
            'level', 'region', 'english'
        ).prefetch_related(
            'skills', 'working_hours'
        ).order_by('last_name', 'first_name')

        g = self.request.GET

        # ── Full-text search ──────────────────────────────────────────────
        q = g.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)  |
                Q(email__icontains=q)      |
                Q(phone__icontains=q)      |
                Q(telegram__icontains=q)
            )

        # ── Row 1 filters ─────────────────────────────────────────────────
        english = g.getlist('english')
        if english:
            qs = qs.filter(english_id__in=english)

        created_from = g.get('created_from', '').strip()
        created_to   = g.get('created_to', '').strip()
        if created_from:
            qs = qs.filter(created_at__date__gte=created_from)
        if created_to:
            qs = qs.filter(created_at__date__lte=created_to)

        exp_from = g.get('exp_from', '').strip()
        exp_to   = g.get('exp_to', '').strip()
        if exp_from:
            qs = qs.filter(work_experience__gte=int(exp_from))
        if exp_to:
            qs = qs.filter(work_experience__lte=int(exp_to))

        salary_currency = g.get('salary_currency', '').strip()
        salary_from     = g.get('salary_from', '').strip()
        salary_to       = g.get('salary_to', '').strip()
        if salary_currency:
            qs = qs.filter(salary_currency=salary_currency)
        if salary_from:
            qs = qs.filter(salary_desired__gte=int(salary_from))
        if salary_to:
            qs = qs.filter(salary_desired__lte=int(salary_to))

        # ── Row 2 filters ─────────────────────────────────────────────────
        skills = g.getlist('skills')
        if skills:
            qs = qs.filter(skills__id__in=skills).distinct()

        level = g.getlist('level')
        if level:
            qs = qs.filter(level_id__in=level)

        region = g.getlist('region')
        if region:
            qs = qs.filter(region_id__in=region)

        working_hours = g.getlist('working_hours')
        if working_hours:
            qs = qs.filter(working_hours__id__in=working_hours).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = PersonSearchForm(self.request.GET)
        ctx['total_count'] = self.get_queryset().count()

        # Pass raw GET values so the template can detect active filters
        g = self.request.GET
        ctx['has_filters'] = any([
            g.get('q'), g.getlist('english'), g.get('created_from'),
            g.get('created_to'), g.get('exp_from'), g.get('exp_to'),
            g.get('salary_currency'), g.get('salary_from'), g.get('salary_to'),
            g.getlist('skills'), g.getlist('level'),
            g.getlist('region'), g.getlist('working_hours'),
        ])
        return ctx


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'people/detail.html'
    context_object_name = 'person'

    def get_queryset(self):
        return Person.objects.select_related(
            'gender', 'level', 'english', 'region'
        ).prefetch_related('skills', 'working_hours', 'working_place')


class PersonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'people/form.html'
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
