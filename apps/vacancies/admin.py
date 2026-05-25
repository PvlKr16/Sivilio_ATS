"""Admin for the Vacancies module."""

from django.contrib import admin
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display   = ['title', 'company', 'status', 'level', 'main_skill',
                      'salary_display', 'for_freelancers', 'created_at']
    list_filter    = ['status', 'for_freelancers', 'level', 'company']
    search_fields  = ['title', 'company__name']
    filter_horizontal = ['skills', 'working_place', 'working_hours', 'supervisors']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Main', {
            'fields': ('status', 'company', 'title'),
        }),
        ('Requirements', {
            'fields': ('level', 'english', 'main_skill', 'skills',
                       'working_place', 'working_hours'),
        }),
        ('Salary', {
            'fields': (('salary_offered', 'salary_currency'),),
        }),
        ('Details', {
            'fields': ('for_freelancers', 'screening', 'supervisors'),
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
