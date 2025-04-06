from django.db import models
from django.utils import timezone
from Auths.models import CustomUser
from ProposeIdea.models import Idea

class DashboardIdea(models.Model):
    """
    Model that integrates the ideas from the ProposeIdea app into the IdeaHubDashboard.
    Stores metadata about how each idea should be displayed on the dashboard.
    """
    idea = models.OneToOneField(
        Idea,
        on_delete=models.CASCADE,
        related_name='dashboard_entry',
        verbose_name="Idea",
        help_text="The idea associated with this dashboard entry."
    )
    featured = models.BooleanField(
        default=False,
        verbose_name="Featured",
        help_text="Mark this idea as featured on the dashboard."
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Control the order in which ideas appear on the dashboard."
    )
    pinned = models.BooleanField(
        default=False,
        verbose_name="Pinned",
        help_text="Pin this idea to the top of the dashboard feed."
    )
    last_accessed = models.DateTimeField(
        default=timezone.now,
        verbose_name="Last Accessed",
        help_text="When this idea was last accessed or updated on the dashboard."
    )

    class Meta:
        verbose_name = "Dashboard Idea"
        verbose_name_plural = "Dashboard Ideas"
        ordering = ['display_order', '-last_accessed']

    def __str__(self):
        return f"Dashboard Entry for: {self.idea.title}"


class IdeaView(models.Model):
    """
    Tracks when a user views an idea in detail. Integrates with Auths (CustomUser) and
    the Idea model from ProposeIdea.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='idea_views',
        verbose_name="User",
        help_text="The user who viewed the idea."
    )
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name="Idea",
        help_text="The idea that was viewed."
    )
    viewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Viewed At",
        help_text="Timestamp when the idea was viewed."
    )

    class Meta:
        verbose_name = "Idea View"
        verbose_name_plural = "Idea Views"
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.username} viewed {self.idea.title} at {self.viewed_at}"


class IdeaInteraction(models.Model):
    """
    Model representing different interactions (like votes, discussions started,
    and tracking activities) that users perform on ideas.
    This connects the Idea model from ProposeIdea and the CustomUser from Auths.
    """
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('discussion', 'Discussion'),
        ('vote', 'Vote'),
        ('track', 'Track'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='idea_interactions',
        verbose_name="User",
        help_text="The user who interacted with the idea."
    )
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name='interactions',
        verbose_name="Idea",
        help_text="The idea that received the interaction."
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=INTERACTION_TYPES,
        verbose_name="Interaction Type",
        help_text="The type of interaction performed by the user."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the interaction occurred."
    )

    class Meta:
        verbose_name = "Idea Interaction"
        verbose_name_plural = "Idea Interactions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} {self.interaction_type} on {self.idea.title}"


class IdeaAttachment(models.Model):
    """
    For displaying attachments in a structured way on the IdeaHubDashboard.
    References Idea’s attachments and allows for organized display.
    """
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name='dashboard_attachments',
        verbose_name="Idea",
        help_text="The idea to which this attachment belongs."
    )
    file = models.FileField(
        upload_to='idea_dashboard_attachments/',
        null=True,
        blank=True,
        verbose_name="Attachment",
        help_text="Attachment file displayed on the dashboard in detail view."
    )
    caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Caption",
        help_text="A short caption or description for this attachment."
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order",
        help_text="Control the order in which attachments appear in the detail view."
    )

    class Meta:
        verbose_name = "Idea Attachment (Dashboard)"
        verbose_name_plural = "Idea Attachments (Dashboard)"
        ordering = ['order']

    def __str__(self):
        return f"Attachment for {self.idea.title} - Order {self.order}"


class IdeaDashboardUserState(models.Model):
    """
    Model to store user-specific state related to the IdeaHubDashboard interface.

    The IdeaHubDashboard.js maintains:
    - activePage: Which page/tab the user is viewing ('dashboard', 'propose', 'tracking', etc.)
    - selectedIdea: The currently selected idea's details when a user clicks "read more"
    - Minimizing behavior: The user can minimize the detailed view and return to the dashboard.

    This model allows for persistence of such state if needed (e.g., restoring user state or analytics).
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='dashboard_state',
        verbose_name="User",
        help_text="The user whose dashboard state is tracked."
    )
    active_page = models.CharField(
        max_length=50,
        default="dashboard",
        verbose_name="Active Page",
        help_text="The current active tab/page the user is viewing."
    )
    selected_idea = models.ForeignKey(
        Idea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selected_by_users',
        verbose_name="Selected Idea",
        help_text="The idea currently selected by the user (if any)."
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated",
        help_text="Timestamp of the last update to the user's dashboard state."
    )

    class Meta:
        verbose_name = "Idea Dashboard User State"
        verbose_name_plural = "Idea Dashboard User States"

    def __str__(self):
        return f"Dashboard state for {self.user.username}"
