from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.urls import path, reverse
from django.shortcuts import redirect

from django_sage_meta.repository import SyncService
from django_sage_meta.models import InstagramAccount, Story


class StoryInline(admin.TabularInline):
    model = Story
    extra = 0
    readonly_fields = ("story_id", "media_type", "media_url", "timestamp")
    can_delete = False


@admin.register(InstagramAccount)
class InstagramAccountAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/insta.html"
    list_display = (
        "id",
        "account_id",
        "username",
        "followers_counts",
        "follows_counts",
    )
    search_fields = ("account_id", "username", "biography")
    search_help_text = _("Search by Account ID, Username, or Biography")
    list_filter = ("followers_counts", "follows_counts", "media_counts")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "account_id",
                    "username",
                    "follows_counts",
                    "followers_counts",
                    "media_counts",
                    "profile_picture_url",
                    "website",
                    "biography",
                )
            },
        ),
    )
    inlines = [StoryInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-insta/",
                self.admin_site.admin_view(self.sync_insta_business),
                name="sync_insta",
            )
        ]
        return custom_urls + urls

    def sync_insta_business(self, request):
        try:
            SyncService.sync_instagram_accounts()
            self.message_user(
                request, _("Instagram accounts synchronized successfully.")
            )
            change_list_url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
            )
            return redirect(change_list_url)
        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
            return HttpResponse(f"An error occurred: {e}", status=500)
