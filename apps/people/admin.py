"""Admin registration for the People module."""

from django.contrib import admin
from .models import Person, Education, Work, PeopleStatus, EducationLevel


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    fields = ['level', 'institution', 'specialization', 'year_start', 'year_end']


class WorkInline(admin.TabularInline):
    model = Work
    extra = 0
    fields = ['employer', 'position', 'date_start', 'date_end', 'is_current']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display  = ['name', 'company', 'position', 'email', 'phone', 'status', 'created_at']
    list_filter   = ['status', 'company', 'title']
    search_fields = ['name', 'email', 'phone', 'uid', 'position']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    inlines       = [EducationInline, WorkInline]
    fieldsets = (
        ('Identity', {
            'fields': ('title', 'name', 'appellative', 'gender', 'uid', 'birthday', 'avatar')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Employment', {
            'fields': ('company', 'position', 'status')
        }),
        ('Notes', {
            'fields': ('obs',)
        }),
        ('Audit', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PeopleStatus)
class PeopleStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active']
    list_editable = ['color', 'is_active']


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    ordering = ['order']
