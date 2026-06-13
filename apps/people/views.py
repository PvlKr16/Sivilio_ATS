"""
Views for the People module.
Full CRUD for Person records.
CV autofill via Cloudflare Worker → Anthropic API.
"""

import base64
import json
import logging
import urllib.request
import urllib.error

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Person, Level, English, Region, Skill
from .forms import PersonForm, PersonSearchForm, PersonFileFormSet

logger = logging.getLogger(__name__)


# ── Mixin: attach file formset to Create / Update ─────────────────────────────

class PersonFileFormSetMixin:
    """Adds PersonFileFormSet handling to any CreateView / UpdateView."""

    def get_file_formset(self, **kwargs):
        instance = getattr(self, 'object', None)
        if self.request.method in ('POST', 'PUT'):
            return PersonFileFormSet(
                self.request.POST,
                self.request.FILES,
                instance=instance,
                prefix='files',
                **kwargs,
            )
        return PersonFileFormSet(instance=instance, prefix='files', **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'file_formset' not in ctx:
            ctx['file_formset'] = self.get_file_formset()
        return ctx

    def form_valid(self, form):
        file_formset = self.get_file_formset()
        if not file_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, file_formset=file_formset)
            )
        self.object = form.save()
        file_formset.instance = self.object
        file_formset.save()
        messages.success(
            self.request,
            _('Person "%(name)s" saved.') % {'name': self.object.full_name},
        )
        return HttpResponseRedirect(self.get_success_url())


# ── List ──────────────────────────────────────────────────────────────────────

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

        q = g.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)  |
                Q(email__icontains=q)      |
                Q(phone__icontains=q)      |
                Q(telegram__icontains=q)
            )

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
        g = self.request.GET
        ctx['has_filters'] = any([
            g.get('q'), g.getlist('english'), g.get('created_from'),
            g.get('created_to'), g.get('exp_from'), g.get('exp_to'),
            g.get('salary_currency'), g.get('salary_from'), g.get('salary_to'),
            g.getlist('skills'), g.getlist('level'),
            g.getlist('region'), g.getlist('working_hours'),
        ])
        return ctx


# ── Detail ────────────────────────────────────────────────────────────────────

class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'people/detail.html'
    context_object_name = 'person'

    def get_queryset(self):
        return Person.objects.select_related(
            'gender', 'level', 'english', 'region'
        ).prefetch_related('skills', 'working_hours', 'working_place', 'files')


# ── Create ────────────────────────────────────────────────────────────────────

class PersonCreateView(
    PersonFileFormSetMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Person
    form_class = PersonForm
    template_name = 'people/form.html'
    permission_required = 'people.add_person'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = _('Create')
        return ctx


# ── Update ────────────────────────────────────────────────────────────────────

class PersonUpdateView(
    PersonFileFormSetMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model               = Person
    form_class          = PersonForm
    template_name       = 'people/form.html'
    permission_required = 'people.change_person'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = _('Edit')
        return ctx


# ── Delete ────────────────────────────────────────────────────────────────────

class PersonDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model               = Person
    template_name       = 'people/confirm_delete.html'
    success_url         = reverse_lazy('people:index')
    permission_required = 'people.delete_person'
    context_object_name = 'person'

    def form_valid(self, form):
        messages.success(self.request, _('Person deleted.'))
        return super().form_valid(form)


# ── Autocomplete ──────────────────────────────────────────────────────────────

def person_autocomplete(request):
    """JSON autocomplete endpoint for person name search."""
    q = request.GET.get('q', '')
    people = Person.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )[:20]
    return JsonResponse({'results': [{'id': p.pk, 'text': p.full_name} for p in people]})


# ── CV Parse ──────────────────────────────────────────────────────────────────

@login_required
@require_POST
def parse_cv(request):
    """
    Accepts a PDF file, forwards it to the Cloudflare Worker proxy,
    which calls Anthropic API and returns structured JSON for form autofill.
    """
    pdf_file = request.FILES.get('cv_file')
    if not pdf_file:
        return JsonResponse({'error': 'No file provided.'}, status=400)
    if not pdf_file.name.lower().endswith('.pdf'):
        return JsonResponse({'error': 'Only PDF files are allowed.'}, status=400)

    # ── Build lookup tables so Claude matches to existing DB values ────────
    level_display   = [{'id': l['id'], 'label': _level_display(l['name'])}
                       for l in Level.objects.values('id', 'name')]
    english_display = [{'id': e['id'], 'label': _english_display(e['name'])}
                       for e in English.objects.values('id', 'name')]
    region_display  = [{'id': r['id'], 'label': r['name']}
                       for r in Region.objects.values('id', 'name')]
    skill_display   = [{'id': s['id'], 'label': s['name']}
                       for s in Skill.objects.values('id', 'name')]

    prompt = f"""You are an HR assistant. Analyze this CV/resume PDF and extract candidate information.

Return ONLY a valid JSON object (no markdown, no explanation) with these keys:
{{
  "first_name": "string or null",
  "last_name": "string or null",
  "email": "string or null",
  "phone": "string or null",
  "telegram": "string (username without @, or null)",
  "linkedin": "string (full URL or null)",
  "profession": "string (job title / desired position, or null)",
  "level_id": integer or null,
  "skill_ids": [list of integers] or [],
  "work_experience": integer (years, or null),
  "education": "string or null",
  "salary_desired": number or null,
  "salary_currency": "USD" | "EUR" | "UAH" | "RUB" | "GBP" | null,
  "region_id": integer or null,
  "english_id": integer or null
}}

Rules:
- For level_id, match to one of: {json.dumps(level_display)}
- For english_id, match to one of: {json.dumps(english_display)}
- For region_id, match to one of: {json.dumps(region_display)}
- For skill_ids, match skills from: {json.dumps(skill_display)}
- If a value cannot be determined, use null (not empty string).
- For phone, include country code if present, keep original formatting.
- For telegram, extract username from t.me/username or @username format.
- For linkedin, return the full profile URL.
- For salary_currency, if salary mentioned without currency, infer from region/language context.
- Return only the JSON object, nothing else."""

    pdf_base64 = base64.standard_b64encode(pdf_file.read()).decode('utf-8')

    # ── Call Cloudflare Worker ─────────────────────────────────────────────
    worker_url    = getattr(settings, 'CF_WORKER_URL', '').rstrip('/') + '/parse-cv'
    worker_secret = getattr(settings, 'CF_WORKER_SECRET', '')

    if not worker_url.startswith('http'):
        return JsonResponse({'error': 'CF_WORKER_URL is not configured.'}, status=503)

    payload = json.dumps({'pdf_base64': pdf_base64, 'prompt': prompt}).encode('utf-8')
    req = urllib.request.Request(
        worker_url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'X-Api-Key':    worker_secret,
            'User-Agent':   'Mozilla/5.0 (compatible; HRPlatform/1.0)',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            worker_data = json.loads(resp.read().decode('utf-8'))

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        logger.error('Worker HTTP %s: %s', e.code, body)
        try:
            err_msg = json.loads(body).get('error', 'Worker error.')
        except Exception:
            err_msg = f'Worker returned HTTP {e.code}.'
        return JsonResponse({'error': err_msg}, status=502)

    except urllib.error.URLError as e:
        logger.error('Worker URL error: %s', e.reason)
        return JsonResponse({'error': 'Cannot reach proxy. Check CF_WORKER_URL setting.'}, status=502)

    except Exception:
        logger.exception('parse_cv: unexpected error')
        return JsonResponse({'error': 'Unexpected server error.'}, status=500)

    # ── Parse Claude's JSON response ───────────────────────────────────────
    raw_text = worker_data.get('text', '')
    if not raw_text:
        return JsonResponse({'error': 'Empty response from Claude.'}, status=500)

    if raw_text.startswith('```'):
        raw_text = raw_text.split('\n', 1)[-1].rsplit('```', 1)[0]

    try:
        data = json.loads(raw_text.strip())
    except json.JSONDecodeError as e:
        logger.error('JSON decode error: %s | raw: %.300s', e, raw_text)
        return JsonResponse({'error': 'Could not parse Claude response as JSON.'}, status=500)

    return JsonResponse({'ok': True, 'data': data})


# ── Helpers ────────────────────────────────────────────────────────────────────

def _level_display(name):
    return {
        'junior': 'Junior', 'middle': 'Middle', 'senior': 'Senior',
        'lead': 'Lead', 'head_of': 'Head of', 'architect': 'Architect',
    }.get(name, name)


def _english_display(name):
    return {
        'a1': 'A1 — Beginner',        'a2': 'A2 — Elementary',
        'b1': 'B1 — Intermediate',     'b2': 'B2 — Upper-Intermediate',
        'c1': 'C1 — Advanced',         'c2': 'C2 — Proficient',
    }.get(name, name)
