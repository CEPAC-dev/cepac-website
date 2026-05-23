from django.contrib import admin
from .models import ProjectCategory, Project


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('name', 'location', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'image')
        }),
        ('Project Details', {
            'fields': ('description', 'about', 'location', 'services', 'software_tools')
        }),
        ('Study Elements', {
            'fields': ('key_elements', 'statistical_analysis')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'order')
        }),
    )
