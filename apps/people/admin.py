"""Admin registration for the People module."""

from django.contrib import admin
from .models import (
    Person, Gender, Level, Skill, WorkingHours,
    Region, WorkingPlace, Profession, English,
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'profession', 'level',
                     'region', 'status', 'salary_display', 'created_at']
    list_filter   = ['status', 'level', 'profession', 'region', 'english']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'telegram']
    filter_horizontal = ['skills', 'working_hours', 'working_place']
    fieldsets = (
        ('Identity', {
            'fields': ('first_name', 'last_name', 'gender', 'birthdate'),
        }),
        ('Professional', {
            'fields': ('profession', 'level', 'skills',
                       'english', 'education', 'work_experience'),
        }),
        ('Salary', {
            'fields': (('salary_desired', 'salary_currency'),),
        }),
        ('Location & Schedule', {
            'fields': ('region', 'working_hours', 'working_place'),
        }),
        ('Contacts', {
            'fields': ('email', 'phone', 'linkedin', 'telegram'),
        }),
        ('Meta', {
            'fields': ('status', 'notes', 'cv'),
        }),
    )


# ── Reference models ─────────────────────────────────────────────────────────

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display  = ['name', 'order']
    list_editable = ['order']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(WorkingPlace)
class WorkingPlaceAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(English)
class EnglishAdmin(admin.ModelAdmin):
    list_display  = ['name', 'order']
    list_editable = ['order']
