"""Views for user account management."""

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy
from .models import User
from .forms import UserUpdateForm


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display current user's profile."""
    template_name = 'accounts/profile.html'


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List all system users."""
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 15
    permission_required = 'accounts.view_user'

    def get_queryset(self):
        qs = super().get_queryset().select_related('person')
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(username__icontains=q) | qs.filter(email__icontains=q)
        return qs


class UserDetailView(LoginRequiredMixin, DetailView):
    """Display user detail page."""
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit user account."""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    permission_required = 'accounts.change_user'

    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={'pk': self.object.pk})
