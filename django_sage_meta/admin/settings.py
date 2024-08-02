from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("id", "access_token", "business_account_id", "user_id")
    search_fields = ("access_token", "business_account_id", "user_id")
    search_help_text = _("Search by Access Token, Business Account ID, or User ID")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "access_token",
                    "business_account_id",
                    "user_id",
                    "messenger_token",
                )
            },
        ),
    )
