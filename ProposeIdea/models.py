from django.db import models
from django.utils import timezone
from Auths.models import CustomUser

class Idea(models.Model):
    """
    Model representing a proposed idea submitted by a user.
    """

    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Idea Title",
        help_text="Enter a compelling title for your idea."
    )
    problem = models.TextField(
        verbose_name="Problem Addressed",
        help_text="Describe the problem your idea aims to solve."
    )
    solution = models.TextField(
        verbose_name="Proposed Solution",
        help_text="Provide a detailed solution for the problem."
    )
    resources = models.TextField(
        verbose_name="Estimated Resources Required",
        help_text="List the resources needed to implement your idea."
    )
    alignment = models.TextField(
        verbose_name="Alignment with Goals",
        help_text="Explain how this idea aligns with the organization's mission."
    )
    tags = models.CharField(
        max_length=255,
        verbose_name="Tags",
        help_text="Enter tags related to your idea, separated by commas."
    )
    attachments = models.FileField(
        upload_to='idea_attachments/',
        null=True,
        blank=True,
        verbose_name="Attachments",
        help_text="Optional. Upload relevant files or images."
    )
    proposer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='proposed_ideas',
        verbose_name="Proposer",
        help_text="The user who proposed this idea."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Submitted',
        verbose_name="Status",
        help_text="Current status of the idea."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the idea was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Timestamp when the idea was last updated."
    )

    class Meta:
        verbose_name = "Idea"
        verbose_name_plural = "Ideas"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
