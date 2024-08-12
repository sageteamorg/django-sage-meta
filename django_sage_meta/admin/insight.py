from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect

from django_sage_meta.models import Insight
from django_sage_meta.repository import SyncService


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/insight.html"
    list_display = ("id", "insight_id", "name", "period", "title")
    search_fields = ("insight_id", "name", "title")
    search_help_text = _("Search by Insight ID, Name, or Title")
    list_filter = ("period", "title", "description")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "insight_id",
                    "name",
                    "period",
                    "values",
                    "title",
                    "description",
                )
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-insights/",
                self.admin_site.admin_view(self.sync_insights),
                name="sync_insights",
            )
        ]
        return custom_urls + urls

    def sync_insights(self, request):
        try:
            SyncService.sync_insights()
            self.message_user(
                request, _("Instagram insights synchronized successfully.")
            )
            change_list_url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
            )
            return redirect(change_list_url)
        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
