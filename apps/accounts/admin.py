"""Admin configuration for User model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('HR Link', {'fields': ('person',)}),
    )
