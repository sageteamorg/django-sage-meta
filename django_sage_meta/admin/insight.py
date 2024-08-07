from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import Insight


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    save_on_top = True
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
