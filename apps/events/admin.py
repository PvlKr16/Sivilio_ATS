"""Admin for the Events module."""

from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ['event_type', 'candidate', 'vacancy', 'company',
                     'event_date', 'event_time', 'supervisor', 'created_at']
    list_filter   = ['event_type', 'company', 'supervisor']
    search_fields = ['candidate__first_name', 'candidate__last_name',
                     'vacancy__title', 'notes']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Event', {
            'fields': ('event_type', 'candidate', 'vacancy', 'company'),
        }),
        ('Schedule', {
            'fields': ('event_date', 'event_time', 'supervisor'),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
