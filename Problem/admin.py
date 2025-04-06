# problem/admin.py

from django.contrib import admin
from .models import Problem, MediaFile
from Auths.models import CustomUser  # Importing CustomUser if needed for display

class MediaFileInline(admin.TabularInline):
    """
    Inline admin interface for MediaFile model.
    Allows uploading and managing media files associated with a Problem directly from the Problem admin page.
    """
    model = MediaFile
    extra = 1  # Number of extra empty forms to display
    readonly_fields = ('uploaded_at',)  # Make 'uploaded_at' read-only
    can_delete = True  # Allow deletion of media files
    verbose_name = "Media File"
    verbose_name_plural = "Media Files"
    # Optionally, you can restrict the number of media files per problem
    # max_num = 10

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Problem model.
    Allows viewing and managing problem submissions, including the 'sdg' field and associated media files.
    """

    # Display these fields in the list view
    list_display = (
        "problem_title",
        "submitter",       # Display the user who submitted the problem
        "category",
        "urgency",
        "sdg",             # Display the SDG field
        "country",
        "city",
        "contact_email",
        "date_created",
    )

    # Enable searching by these fields
    search_fields = (
        "problem_title",
        "description",
        "category",
        "contact_name",
        "contact_email",
        "contact_phone",
        "sdg",  # Allow searching by SDG
        # Also allow searching by the submitter's email via the related model:
        "submitter__email",
        # If you wish to also search by username, you can add:
        # "submitter__username",
    )

    # Enable filtering by these fields
    list_filter = (
        "category",
        "urgency",
        "sdg",             # Add SDG to the filter sidebar
        "country",
        "city",
        "date_created",
        "submitter",       # Optionally filter by submitter
    )

    # Make 'date_created' read-only to prevent editing
    readonly_fields = ("date_created",)

    # Organize fields into logical sections using fieldsets
    fieldsets = (
        ("Problem Details", {
            "fields": (
                "submitter",        # Display the submitter in the first section
                "problem_title",
                "description",
                "category",
                "urgency",
                "sdg",              # Include SDG in the Problem Details
            )
        }),
        ("Location Info", {
            "fields": (
                "country",
                "city",
                "latitude",
                "longitude",
            )
        }),
        ("Media", {
            "fields": (
                "submitter_photo",  # Display the submitter's photo
            ),
            "classes": ('collapse',),  # Optionally collapse the media section for better UX
        }),
        ("Contact Info", {
            "fields": (
                "contact_name",
                "contact_email",
                "contact_phone",
            )
        }),
        ("Timestamps", {
            "fields": (
                "date_created",
            )
        }),
    )

    # Include the MediaFile inline for managing media files directly from the Problem admin page
    inlines = [MediaFileInline]

    # Optionally, you can display related media files in the list view using list_display_links or list_select_related
    # However, since media_files are handled via inlines, it's generally not necessary

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MediaFile model.
    Allows viewing and managing media files independently if needed.
    """
    list_display = ("id", "problem", "file", "uploaded_at")
    search_fields = ("problem__problem_title", "file")
    list_filter = ("uploaded_at", "problem__sdg", "problem__category")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)

    # Optionally, you can add a link to the related Problem in the list display
    def problem_link(self, obj):
        """
        Returns a link to the associated Problem in the admin interface.
        """
        if obj.problem:
            url = f"/admin/problem/problem/{obj.problem.id}/change/"
            return format_html('<a href="{}">{}</a>', url, obj.problem.problem_title)
        return "-"
    problem_link.short_description = "Problem"

    list_display = ("id", "problem_link", "file", "uploaded_at")

    # If you want to restrict how MediaFiles are added or edited, you can customize form fields here

