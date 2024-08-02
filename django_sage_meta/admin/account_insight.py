from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from django_sage_meta.models import AccountInsight
from django_sage_meta.resources import AccountInsightResource

@admin.register(AccountInsight)
class AccountInsightAdmin(ImportExportModelAdmin):
    resource_class = AccountInsightResource
    save_on_top = True
    list_display = ("id", "account_insight_id", "name", "period", "title")
    search_fields = ("account_insight_id", "name", "title")
    search_help_text = _("Search by Account Insight ID, Name, or Title")
    list_filter = ("period", "title", "description")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "account_insight_id",
                    "name",
                    "period",
                    "values",
                    "title",
                    "description",
                )
            },
        ),
    )
    autocomplete_fields = ["category"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync-values/', self.admin_site.admin_view(self.sync_values), name='sync_values'),
        ]
        return custom_urls + urls

    def sync_values(self, request):
        # Add your sync logic here
        self.message_user(request, "Values have been synced.")
        return HttpResponseRedirect(reverse('admin:app_accountinsight_changelist'))
