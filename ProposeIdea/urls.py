from django.urls import path
from .views import (
    IdeaCreateAPIView,
    IdeaListAPIView,
    IdeaDetailAPIView,
    IdeaStatusUpdateAPIView,
)

urlpatterns = [
    # Endpoint to create a new idea
    path('submit/', IdeaCreateAPIView.as_view(), name='idea-create'),

    # Endpoint to list all ideas or filter by proposer
    path('', IdeaListAPIView.as_view(), name='idea-list'),

    # Endpoint to retrieve, update, or delete a specific idea
    path('<int:pk>/', IdeaDetailAPIView.as_view(), name='idea-detail'),

    # Endpoint for admin users to update the status of an idea
    path('<int:pk>/status/', IdeaStatusUpdateAPIView.as_view(), name='idea-status-update'),
]
