from rest_framework import serializers
from Auths.models import CustomUser
from ProposeIdea.models import Idea
from .models import DashboardIdea, IdeaView, IdeaInteraction, IdeaAttachment, IdeaDashboardUserState

class IdeaAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for IdeaAttachment model.
    This will help display attachments in the dashboard's detailed view,
    similar to how IdeaHubDashboard.js shows attachments.
    """
    class Meta:
        model = IdeaAttachment
        fields = ['id', 'file', 'caption', 'order']


class IdeaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Idea model (from ProposeIdea) to align with IdeaHubDashboard.js structure.
    IdeaHubDashboard.js expects fields like:
    - id
    - title
    - description (not in Idea model, so we'll create a method field)
    - attachments
    - problem
    - solution
    - resources
    - alignment
    - tags

    We'll map 'description' to something suitable (e.g., a truncated problem or a summary).
    Since the original code uses 'description' in the ideas array, we can assume it might be a short summary
    or first line of the problem. We'll provide a method field for that.
    """
    description = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    def get_description(self, obj):
        # If no dedicated 'description' field in the Idea model, we can derive it from problem or solution.
        # For simplicity, use the first 100 chars of the problem as 'description'.
        return (obj.problem[:100] + '...') if len(obj.problem) > 100 else obj.problem

    def get_attachments(self, obj):
        # If we have IdeaAttachment objects, we can serialize them. Otherwise, fallback to the single attachments file.
        # The code in IdeaHubDashboard.js expects a single attachments field as a string (URL),
        # but we have a file field in Idea and multiple attachments in IdeaAttachment model.
        # We'll try IdeaAttachment first, if none found, fallback to obj.attachments (from Idea model).
        dashboard_attachments = obj.dashboard_attachments.all().order_by('order')
        if dashboard_attachments.exists():
            # Return the first attachment's file URL as the primary attachment to align with IdeaHubDashboard.js expectation
            return dashboard_attachments.first().file.url if dashboard_attachments.first().file else None
        # If no dashboard attachments are found, use the original idea.attachments field if it exists
        return obj.attachments.url if obj.attachments else None

    class Meta:
        model = Idea
        fields = [
            'id', 'title', 'description', 'attachments',
            'problem', 'solution', 'resources', 'alignment', 'tags'
        ]


class DashboardIdeaSerializer(serializers.ModelSerializer):
    """
    Serializer for DashboardIdea model, integrating Idea data and dashboard metadata.
    This helps manage featured, pinned, order info, etc.
    """
    idea = IdeaSerializer(read_only=True)

    class Meta:
        model = DashboardIdea
        fields = [
            'id', 'idea', 'featured', 'display_order', 'pinned', 'last_accessed'
        ]


class IdeaViewSerializer(serializers.ModelSerializer):
    """
    Serializer for IdeaView model, tracking when users view an idea.
    Useful if we need to display how many views an idea has or user-specific analytics.
    """
    user = serializers.CharField(source='user.username', read_only=True)
    idea = serializers.CharField(source='idea.title', read_only=True)

    class Meta:
        model = IdeaView
        fields = ['id', 'user', 'idea', 'viewed_at']


class IdeaInteractionSerializer(serializers.ModelSerializer):
    """
    Serializer for IdeaInteraction model.
    Tracks user interactions like 'discussion', 'vote', 'track' on an idea.
    """
    user = serializers.CharField(source='user.username', read_only=True)
    idea = serializers.CharField(source='idea.title', read_only=True)

    class Meta:
        model = IdeaInteraction
        fields = ['id', 'user', 'idea', 'interaction_type', 'created_at']


class IdeaDashboardUserStateSerializer(serializers.ModelSerializer):
    """
    Serializer for IdeaDashboardUserState model to store/restore user state.
    IdeaHubDashboard.js maintains state like:
    - activePage
    - selectedIdea (if any)
    - Minimizing behavior (not explicitly stored, but we can handle selected_idea as null)

    This serializer can help persist user state if needed.
    """
    user = serializers.CharField(source='user.username', read_only=True)
    selected_idea = serializers.SerializerMethodField()

    def get_selected_idea(self, obj):
        if obj.selected_idea:
            # Return a subset of idea fields useful for quick restore
            return {
                'id': obj.selected_idea.id,
                'title': obj.selected_idea.title,
                'problem': obj.selected_idea.problem,
                'solution': obj.selected_idea.solution,
                'resources': obj.selected_idea.resources,
                'alignment': obj.selected_idea.alignment,
                'tags': obj.selected_idea.tags,
                'attachments': obj.selected_idea.attachments.url if obj.selected_idea.attachments else None
            }
        return None

    class Meta:
        model = IdeaDashboardUserState
        fields = [
            'id', 'user', 'active_page', 'selected_idea', 'last_updated'
        ]


class IdeaAttachmentDashboardSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for dashboard attachments from IdeaAttachment model.
    If we need to list all attachments in detail view, this serializer can be used.
    """
    idea = serializers.CharField(source='idea.title', read_only=True)

    class Meta:
        model = IdeaAttachment
        fields = ['id', 'idea', 'file', 'caption', 'order']


# If needed, we can create a combined serializer that gathers all data that IdeaHubDashboard.js might need
# for a single request, but usually the frontend will call separate endpoints for idea lists, details, etc.
