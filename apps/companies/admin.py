"""Admin for the Companies module."""

from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display   = ['name', 'email', 'phone', 'contact_person',
                      'payment_options', 'amount', 'status', 'created_at']
    list_filter    = ['status', 'payment_options']
    search_fields  = ['name', 'email', 'phone']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'email', 'phone', 'contact_person'),
        }),
        ('Commercial', {
            'fields': ('payment_options', 'amount', 'status'),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
