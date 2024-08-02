from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_sage_meta.models import AccountInsight


@admin.register(AccountInsight)
class AccountInsightAdmin(admin.ModelAdmin):
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

