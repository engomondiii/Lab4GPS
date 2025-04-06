# problem/serializers.py

from rest_framework import serializers
from Auths.models import CustomUser
from .models import Problem, MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the MediaFile model to handle media uploads and retrievals.
    """
    class Meta:
        model = MediaFile
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ProblemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Problem model, now including nested MediaFile uploads
    and handling the new Sustainable Development Goal (SDG) field.
    """
    submitter = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True,
        help_text="If the user is logged in, link to their CustomUser account."
    )
    media_files = MediaFileSerializer(many=True, read_only=True)
    media_files_upload = serializers.ListField(
        child=serializers.FileField(
            max_length=1000000, 
            allow_empty_file=False, 
            use_url=False
        ),
        write_only=True,
        required=False,
        help_text="List of media files (images, videos) to upload."
    )

    class Meta:
        model = Problem
        fields = [
            "id",
            "submitter",
            "problem_title",
            "description",
            "category",
            "urgency",
            "sdg",  # **Added SDG Field**
            "country",
            "city",
            "latitude",
            "longitude",
            "media_files",
            "media_files_upload",
            "submitter_photo",
            "contact_name",
            "contact_email",
            "contact_phone",
            "date_created",
        ]
        read_only_fields = ("id", "date_created", "media_files")

    def validate_sdg(self, value):
        """
        Validate that the provided SDG value is one of the predefined choices.
        """
        sdg_choices = [choice[0] for choice in Problem.SDG_CHOICES]
        if value not in sdg_choices:
            raise serializers.ValidationError("Invalid SDG selected.")
        return value

    def create(self, validated_data):
        """
        Override the create method to handle media file uploads and associate them with the problem.
        """
        media_files = validated_data.pop('media_files_upload', [])
        submitter_photo = validated_data.pop('submitter_photo', None)

        # Create the Problem instance
        problem = Problem.objects.create(submitter=self.context['request'].user if self.context['request'].user.is_authenticated else None,
                                         submitter_photo=submitter_photo,
                                         **validated_data)
        
        # Handle media files upload
        for file in media_files:
            MediaFile.objects.create(problem=problem, file=file)
        
        return problem

    def to_representation(self, instance):
        """
        Customize the representation to include URLs for media files and submitter photo.
        """
        representation = super().to_representation(instance)
        
        # Add submitter_photo URL if it exists
        if instance.submitter_photo:
            representation['submitter_photo_url'] = instance.submitter_photo.url
        else:
            representation['submitter_photo_url'] = None
        
        # Add media_files URLs
        representation['media_files_urls'] = [media.file.url for media in instance.media_files.all()]
        
        # Optionally, format SDG to display both code and title separately
        sdg_code, sdg_title = instance.sdg.split('. ', 1) if '. ' in instance.sdg else ('', instance.sdg)
        representation['sdg_code'] = sdg_code
        representation['sdg_title'] = sdg_title
        
        return representation
