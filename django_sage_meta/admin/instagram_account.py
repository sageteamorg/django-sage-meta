from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import InstagramAccount


@admin.register(InstagramAccount)
class InstagramAccountAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("id", "account_id", "username", "followers_count", "follows_count")
    search_fields = ("account_id", "username", "biography")
    search_help_text = _("Search by Account ID, Username, or Biography")
    list_filter = ("followers_count", "follows_count", "media_count")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "account_id",
                    "username",
                    "follows_count",
                    "followers_count",
                    "media_count",
                    "profile_picture_url",
                    "website",
                    "biography",
                )
            },
        ),
        (
            "Media and Insights",
            {"fields": ("media", "insights", "stories"), "classes": ("collapse",)},
        ),
    )
    autocomplete_fields = ["media", "insights", "stories"]
