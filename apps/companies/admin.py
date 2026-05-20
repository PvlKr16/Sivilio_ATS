"""Admin registration for the Companies module."""

from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'pays_vat', 'is_tenant', 'people_count', 'created_at']
    list_filter   = ['pays_vat', 'is_tenant']
    search_fields = ['name', 'email', 'phone', 'bank', 'bank_account']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'email', 'phone', 'fax', 'logo')
        }),
        ('Legal representative', {
            'fields': ('mandatary',)
        }),
        ('Banking', {
            'fields': ('bank', 'bank_account')
        }),
        ('Flags', {
            'fields': ('pays_vat', 'is_tenant')
        }),
        ('Notes', {
            'fields': ('obs',)
        }),
        ('Audit', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def people_count(self, obj):
        return obj.people.count()
    people_count.short_description = 'People'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
