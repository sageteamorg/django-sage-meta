from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from ..models import InstagramAccount
from ..resources import InstagramAccountResource
from .actions.insta import fetch_and_save_instagram_accounts

@admin.register(InstagramAccount)
class InstagramAccountAdmin(ImportExportModelAdmin):
    resource_class = InstagramAccountResource
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
    actions=[fetch_and_save_instagram_accounts]