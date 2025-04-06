# problem/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Problem
from .serializers import ProblemSerializer

class ProblemViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides:
      - list (GET /problems/problems/): No auth required
      - retrieve (GET /problems/problems/<id>/): No auth required
      - create (POST /problems/problems/): Auth required
      - update, partial_update, destroy (PATCH/PUT/DELETE): Auth required

    Additional filtering:
    - GET /problems/problems/?contact_email=<user_email>
      returns only the problems submitted with that contact email.

    The serializer now handles setting the 'submitter' field based on the authenticated user.
    """
    
    queryset = Problem.objects.all().order_by('-date_created')
    serializer_class = ProblemSerializer

    def get_permissions(self):
        """
        Custom permission handling:
        - list/retrieve actions => no authentication required
        - create/update/partial_update/destroy => must be authenticated
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            # create, update, partial_update, destroy
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Optionally filter problems by 'contact_email' query parameter.
        Example: /problems/problems/?contact_email=john.doe@example.com
        Returns all problems if no query param is provided.
        """
        queryset = super().get_queryset()
        contact_email = self.request.query_params.get('contact_email')
        if contact_email:
            queryset = queryset.filter(contact_email=contact_email)
        return queryset

    