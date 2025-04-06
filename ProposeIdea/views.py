from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Idea
from .serializers import IdeaSerializer


class IdeaCreateAPIView(generics.CreateAPIView):
    """
    API view to create a new idea.
    The authenticated user is automatically set as the proposer.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(proposer=self.request.user)


class IdeaListAPIView(generics.ListAPIView):
    """
    API view to list all ideas.
    Allows filtering based on the proposer's ideas or all ideas.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        proposer_only = self.request.query_params.get('proposer', None)
        if proposer_only == 'true' and self.request.user.is_authenticated:
            return Idea.objects.filter(proposer=self.request.user)
        return super().get_queryset()


class IdeaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific idea.
    Only the proposer of the idea can update or delete it.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Ensure only the proposer can update their idea
        if serializer.instance.proposer != self.request.user:
            return Response(
                {"error": "You do not have permission to update this idea."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure only the proposer can delete their idea
        if instance.proposer != self.request.user:
            return Response(
                {"error": "You do not have permission to delete this idea."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class IdeaStatusUpdateAPIView(generics.UpdateAPIView):
    """
    API view for admin users to update the status of an idea.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()
