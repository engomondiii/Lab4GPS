from django.urls import path
from .views import (
    DashboardIdeaListAPIView,
    DashboardIdeaDetailAPIView,
    IdeaInteractionAPIView,
    IdeaViewRecordAPIView,
    IdeaAttachmentListAPIView,
    IdeaDashboardUserStateAPIView
)

urlpatterns = [
    # List of ideas displayed on the dashboard (dashboard view)
    path('dashboard/', DashboardIdeaListAPIView.as_view(), name='dashboard-ideas'),

    # Detailed view of a single idea (for "Click to read more..." functionality)
    path('ideas/<int:pk>/', DashboardIdeaDetailAPIView.as_view(), name='dashboard-idea-detail'),

    # Record user interactions like discussions, votes, track actions
    path('ideas/interaction/', IdeaInteractionAPIView.as_view(), name='idea-interaction'),

    # Record that a user has viewed an idea (for analytics/user-specific data)
    path('ideas/view/', IdeaViewRecordAPIView.as_view(), name='idea-view-record'),

    # List all attachments for a given idea in detail view
    path('ideas/attachments/', IdeaAttachmentListAPIView.as_view(), name='idea-attachments-list'),

    # Manage and persist user dashboard state (active_page, selected_idea, etc.)
    path('user/state/', IdeaDashboardUserStateAPIView.as_view(), name='idea-dashboard-user-state'),
]
