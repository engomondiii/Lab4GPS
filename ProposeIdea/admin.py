from django.contrib import admin
from .models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    """
    Admin interface for managing ideas.
    """
    list_display = (
        'title', 
        'proposer', 
        'status', 
        'created_at', 
        'updated_at'
    )
    list_filter = (
        'status', 
        'created_at', 
        'updated_at'
    )
    search_fields = (
        'title', 
        'proposer__username', 
        'proposer__email', 
        'tags'
    )
    readonly_fields = (
        'created_at', 
        'updated_at'
    )
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'problem', 
                'solution', 
                'resources', 
                'alignment', 
                'tags', 
                'attachments'
            )
        }),
        ('Proposer Information', {
            'fields': (
                'proposer', 
            )
        }),
        ('Status & Timestamps', {
            'fields': (
                'status', 
                'created_at', 
                'updated_at'
            )
        }),
    )
