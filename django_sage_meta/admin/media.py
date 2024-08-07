from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        "id",
        "media_id",
        "caption",
        "media_type",
        "like_count",
        "comments_count",
        "username",
    )
    search_fields = ("media_id", "caption", "media_type")
    search_help_text = _("Search by Media ID, Caption, or Media Type")
    list_filter = ("media_type", "like_count", "comments_count")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "media_id",
                    "caption",
                    "media_type",
                    "media_url",
                    "timestamp",
                    "like_count",
                    "comments_count",
                )
            },
        ),
        ("Comments", {"fields": ("comments",), "classes": ("collapse",)}),
    )
    autocomplete_fields = ["comments"]
