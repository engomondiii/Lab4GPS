# problem/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProblemViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'problems', ProblemViewSet, basename='problem')

urlpatterns = [
    # The API URLs are determined automatically by the router.
    path('', include(router.urls)),
]
