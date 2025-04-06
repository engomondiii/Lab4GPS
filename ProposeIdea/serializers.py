from rest_framework import serializers
from .models import Idea
from Auths.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    This is used to serialize the proposer field in the Idea model.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture']


class IdeaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Idea model.
    Handles serialization and deserialization of Idea data.
    """
    proposer = CustomUserSerializer(read_only=True)  # Nested proposer details
    attachments = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Idea
        fields = [
            'id', 'title', 'problem', 'solution', 'resources',
            'alignment', 'tags', 'attachments', 'proposer',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Custom create method to set the proposer to the currently authenticated user.
        """
        request = self.context.get('request')  # Access the current request
        validated_data['proposer'] = request.user  # Set the proposer as the authenticated user
        return super().create(validated_data)
