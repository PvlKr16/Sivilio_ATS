"""Admin configuration for the custom User model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['username', 'full_name_display', 'email', 'role',
                     'status', 'works_since', 'is_active', 'is_staff']
    list_filter   = ['status', 'role', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    ordering      = ['last_name', 'first_name']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'avatar',
                       'phone', 'viber', 'telegram'),
        }),
        ('HR info', {
            'fields': ('role', 'status', 'works_since', 'cv'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',
                       'first_name', 'last_name', 'email',
                       'role', 'status', 'works_since'),
        }),
    )

    @admin.display(description='Name')
    def full_name_display(self, obj):
        return obj.get_full_name() or '—'
