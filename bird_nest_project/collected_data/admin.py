from django.contrib import admin
from django.utils.html import mark_safe
from bird_nest_project.collected_data.models import PlottedData
from django.conf import settings


# Register your models here.
@admin.register(PlottedData)
class PlottedDataAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "group_name",
        "file_path",
        "format",
        "latitude",
        "longitude",
        "enriched_data",
    ]
    search_fields = ["group_name", "file_path"]  # Add fields for search functionality
    list_filter = ["group_name", "format"]  # Add filters for list view
    readonly_fields = ["render_image"]

    def render_image(self, obj):
        base_url = (
            settings.MEDIA_URL
        )  # Assuming the images are stored in the media directory
        return mark_safe(
            f'<img src="{base_url}{obj.file_path}" style="max-width: 200px; max-height: 200px;" />'
        )

    render_image.short_description = "Image Preview"
