"""Views for user management and self-service profile."""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import User
from .forms import UserCreateForm, UserUpdateForm, ProfileUpdateForm


class ProfileView(LoginRequiredMixin, UpdateView):
    """Self-service profile page — the logged-in user edits their own data."""
    model         = User
    form_class    = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url   = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        # Always edit the currently logged-in user
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Paginated list of all system users."""
    model               = User
    template_name       = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by         = 15
    permission_required = 'accounts.view_user'

    def get_queryset(self):
        qs = User.objects.select_related('role').order_by('last_name', 'first_name')
        q  = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q)
            )
        role = self.request.GET.get('role', '')
        if role:
            qs = qs.filter(role_id=role)
        status = self.request.GET.get('status', '')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        from django.contrib.auth.models import Group
        ctx = super().get_context_data(**kwargs)
        ctx['roles']      = Group.objects.all()
        ctx['status_choices'] = User.status.field.choices
        return ctx


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a new user account."""
    model               = User
    form_class          = UserCreateForm
    template_name       = 'accounts/user_form.html'
    permission_required = 'accounts.add_user'
    success_url         = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'User "{form.instance.username}" created.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit an existing user account."""
    model               = User
    form_class          = UserUpdateForm
    template_name       = 'accounts/user_form.html'
    permission_required = 'accounts.change_user'
    success_url         = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        messages.success(self.request, f'User "{form.instance.username}" updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx
