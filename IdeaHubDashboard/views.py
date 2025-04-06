from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone

from Auths.models import CustomUser
from ProposeIdea.models import Idea
from .models import (
    DashboardIdea,
    IdeaView,
    IdeaInteraction,
    IdeaAttachment,
    IdeaDashboardUserState
)
from .serializers import (
    DashboardIdeaSerializer,
    IdeaSerializer,
    IdeaViewSerializer,
    IdeaInteractionSerializer,
    IdeaAttachmentDashboardSerializer,
    IdeaDashboardUserStateSerializer
)


class DashboardIdeaListAPIView(generics.ListAPIView):
    """
    Returns a list of ideas to display on the IdeaHubDashboard.
    Corresponds to the dashboard view in IdeaHubDashboard.js,
    which expects a list of ideas with fields like title, description, tags, etc.
    """
    queryset = DashboardIdea.objects.select_related('idea').order_by('display_order', '-last_accessed')
    serializer_class = DashboardIdeaSerializer
    permission_classes = [permissions.AllowAny]


class DashboardIdeaDetailAPIView(APIView):
    """
    Returns detailed information for a single idea.
    Aligns with the "click to read more..." functionality in IdeaHubDashboard.js.
    When a user clicks "read more", the frontend navigates to an idea detail view.
    This endpoint provides full details including problem, solution, resources, alignment, tags, and attachments.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        idea = get_object_or_404(Idea, pk=pk)
        # Serialize the Idea with full details
        serializer = IdeaSerializer(idea)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdeaInteractionAPIView(APIView):
    """
    Handles user interactions such as 'discussion', 'vote', 'track' on an idea.
    In IdeaHubDashboard.js, when user clicks on Discussion, Vote, Track,
    it might trigger a call to record this interaction for analytics or future state restoration.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        idea_id = request.data.get('idea_id')
        interaction_type = request.data.get('interaction_type')

        if not idea_id or not interaction_type:
            return Response({"detail": "idea_id and interaction_type are required."}, status=status.HTTP_400_BAD_REQUEST)

        idea = get_object_or_404(Idea, pk=idea_id)
        if interaction_type not in dict(IdeaInteraction.INTERACTION_TYPES):
            return Response({"detail": "Invalid interaction type."}, status=status.HTTP_400_BAD_REQUEST)

        interaction = IdeaInteraction.objects.create(user=user, idea=idea, interaction_type=interaction_type)
        serializer = IdeaInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IdeaViewRecordAPIView(APIView):
    """
    Records that a user viewed an idea. The frontend might call this endpoint when a user 
    navigates to the idea detail view. This aligns with IdeaHubDashboard.js behavior if we want
    to track view counts or user-specific analytics.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        idea_id = request.data.get('idea_id')

        if not idea_id:
            return Response({"detail": "idea_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        idea = get_object_or_404(Idea, pk=idea_id)
        idea_view = IdeaView.objects.create(user=user, idea=idea)
        serializer = IdeaViewSerializer(idea_view)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IdeaAttachmentListAPIView(generics.ListAPIView):
    """
    Returns all attachments for a given idea in a structured manner.
    If IdeaHubDashboard.js needs to load more attachments in detail view, this endpoint can be used.
    """
    serializer_class = IdeaAttachmentDashboardSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        idea_id = self.request.query_params.get('idea_id')
        if not idea_id:
            return IdeaAttachment.objects.none()
        return IdeaAttachment.objects.filter(idea_id=idea_id).order_by('order')


class IdeaDashboardUserStateAPIView(APIView):
    """
    Handles retrieval and update of user-specific dashboard state:
    - active_page (which tab the user is currently on)
    - selected_idea (which idea is currently selected/read)
    
    The IdeaHubDashboard.js file maintains state in the frontend. If we want to persist 
    or restore it from the backend, we can use this endpoint.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_state, created = IdeaDashboardUserState.objects.get_or_create(user=request.user)
        serializer = IdeaDashboardUserStateSerializer(user_state)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_state, created = IdeaDashboardUserState.objects.get_or_create(user=request.user)
        active_page = request.data.get('active_page')
        selected_idea_id = request.data.get('selected_idea_id')

        if active_page:
            user_state.active_page = active_page

        if selected_idea_id:
            selected_idea = get_object_or_404(Idea, pk=selected_idea_id)
            user_state.selected_idea = selected_idea
        else:
            user_state.selected_idea = None

        user_state.save()
        serializer = IdeaDashboardUserStateSerializer(user_state)
        return Response(serializer.data, status=status.HTTP_200_OK)
