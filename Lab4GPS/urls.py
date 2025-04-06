# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Auths app URLs
    path('auth/', include('Auths.urls')),

    # Archive app URLs
    path('archive/', include('Archive.urls')),  # Added Archive app routes

    # ProposeIdea app URLs
    path('ideas/', include('ProposeIdea.urls')),

    # IdeaHubDashboard app URLs
    path('ideadashboard/', include('IdeaHubDashboard.urls')),

    # Problem App URLs
    path('problems/', include('Problem.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
