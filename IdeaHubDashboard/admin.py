from django.contrib import admin
from .models import DashboardIdea, IdeaView, IdeaInteraction, IdeaAttachment, IdeaDashboardUserState

@admin.register(DashboardIdea)
class DashboardIdeaAdmin(admin.ModelAdmin):
    list_display = ('idea', 'featured', 'pinned', 'display_order', 'last_accessed')
    list_filter = ('featured', 'pinned')
    search_fields = ('idea__title',)
    ordering = ('display_order', '-last_accessed')

@admin.register(IdeaView)
class IdeaViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'viewed_at')
    list_filter = ('viewed_at', 'idea__title')
    search_fields = ('user__username', 'idea__title')
    date_hierarchy = 'viewed_at'
    ordering = ('-viewed_at',)

@admin.register(IdeaInteraction)
class IdeaInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'idea', 'interaction_type', 'created_at')
    list_filter = ('interaction_type', 'created_at', 'idea__title')
    search_fields = ('user__username', 'idea__title', 'interaction_type')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(IdeaAttachment)
class IdeaAttachmentAdmin(admin.ModelAdmin):
    list_display = ('idea', 'caption', 'order')
    list_filter = ('idea__title',)
    search_fields = ('idea__title', 'caption')
    ordering = ('order',)

@admin.register(IdeaDashboardUserState)
class IdeaDashboardUserStateAdmin(admin.ModelAdmin):
    list_display = ('user', 'active_page', 'selected_idea', 'last_updated')
    list_filter = ('active_page', 'last_updated')
    search_fields = ('user__username', 'selected_idea__title')
    date_hierarchy = 'last_updated'
    ordering = ('-last_updated',)
