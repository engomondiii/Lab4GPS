# problem/models.py

from django.db import models
from django.utils import timezone
from Auths.models import CustomUser  # Import your CustomUser model

class Problem(models.Model):
    """
    Stores information about user-submitted problems, integrating with the CustomUser model.
    Now handles actual file uploads for media files and submitter photo.
    """

    # Define the 17 Sustainable Development Goals (SDGs) as choices
    SDG_CHOICES = [
        ('1. No Poverty', 'No Poverty'),
        ('2. Zero Hunger', 'Zero Hunger'),
        ('3. Good Health and Well-being', 'Good Health and Well-being'),
        ('4. Quality Education', 'Quality Education'),
        ('5. Gender Equality', 'Gender Equality'),
        ('6. Clean Water and Sanitation', 'Clean Water and Sanitation'),
        ('7. Affordable and Clean Energy', 'Affordable and Clean Energy'),
        ('8. Decent Work and Economic Growth', 'Decent Work and Economic Growth'),
        ('9. Industry, Innovation, and Infrastructure', 'Industry, Innovation, and Infrastructure'),
        ('10. Reduced Inequalities', 'Reduced Inequalities'),
        ('11. Sustainable Cities and Communities', 'Sustainable Cities and Communities'),
        ('12. Responsible Consumption and Production', 'Responsible Consumption and Production'),
        ('13. Climate Action', 'Climate Action'),
        ('14. Life Below Water', 'Life Below Water'),
        ('15. Life on Land', 'Life on Land'),
        ('16. Peace, Justice, and Strong Institutions', 'Peace, Justice, and Strong Institutions'),
        ('17. Partnerships for the Goals', 'Partnerships for the Goals'),
    ]

    # Optional foreign key to CustomUser if the submitter is an authenticated user.
    submitter = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='submitted_problems',
        blank=True,
        null=True,
        verbose_name="Submitter",
        help_text="If the user is logged in, link to their CustomUser account."
    )

    # Core Problem Info
    problem_title = models.CharField(
        max_length=255,
        verbose_name="Problem Title",
        help_text="Title or short description of the problem."
    )
    description = models.TextField(
        verbose_name="Problem Description",
        help_text="Detailed explanation of the problem."
    )

    # Category (includes custom category user may have typed)
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Problem Category",
        help_text="Either a predefined or user-defined category."
    )

    # Urgency Level
    urgency = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High"),
            ("Critical", "Critical"),
        ],
        verbose_name="Urgency Level"
    )

    # **New Field: Sustainable Development Goal (SDG)**
    sdg = models.CharField(
        max_length=50,
        choices=SDG_CHOICES,
        default='1. No Poverty',  # Set a default value
        verbose_name="Sustainable Development Goal (SDG)",
        help_text="The SDG related to the problem.",
    )

    # Location Info
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Country",
        help_text="The country of the problem location."
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="City/Town",
        help_text="The city or town of the problem location."
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Latitude",
        help_text="Decimal latitude of the location."
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Longitude",
        help_text="Decimal longitude of the location."
    )

    # Media & Submitter Photo 
    # Updated to handle actual file uploads
    submitter_photo = models.ImageField(
        upload_to='submitter_photos/',
        blank=True,
        null=True,
        verbose_name="Submitter Photo",
        help_text="Photo of the submitter if provided."
    )

    # Contact Info (kept for non-authenticated or additional references)
    contact_name = models.CharField(
        max_length=100,
        verbose_name="Contact Name"
    )
    contact_email = models.EmailField(
        verbose_name="Contact Email"
    )
    contact_phone = models.CharField(
        max_length=50,
        verbose_name="Contact Phone Number"
    )

    # Timestamps
    date_created = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name="Date Created"
    )

    def __str__(self):
        # Show problem title plus contact or an authenticated user's email
        if self.submitter:
            return f"{self.problem_title} (AuthUser: {self.submitter.email})"
        else:
            return f"{self.problem_title} (Guest: {self.contact_email})"

class MediaFile(models.Model):
    """
    Model to handle multiple media files associated with a Problem.
    """
    problem = models.ForeignKey(
        Problem,
        related_name='media_files',
        on_delete=models.CASCADE,
        verbose_name="Problem",
        help_text="The problem this media file is associated with."
    )
    file = models.FileField(
        upload_to='problem_media/',
        verbose_name="Media File",
        help_text="Image or video file associated with the problem."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Uploaded At",
        help_text="Timestamp when the media file was uploaded."
    )

    def __str__(self):
        return f"MediaFile {self.id} for Problem {self.problem.id}"
