from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from django_sage_meta.models import FacebookPageData
from django_sage_meta.resources import FacebookPageDataResource
from django_sage_meta.admin.actions.page import fetch_and_save_pages


@admin.register(FacebookPageData)
class FacebookPageDataAdmin(ImportExportModelAdmin):
    resource_class = FacebookPageDataResource
    save_on_top = True
    list_display = ("id", "page_id", "name", "category")
    search_fields = ("page_id", "name", "category")
    search_help_text = _("Search by Page ID, Name, or Category")
    list_filter = ("category",)
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("page_id", "name", "category", "access_token")}),
        (
            "Categories and Tasks",
            {"fields": ("categories", "tasks"), "classes": ("collapse",)},
        ),
        (
            "Instagram Business Account",
            {"fields": ("instagram_business_account",), "classes": ("collapse",)},
        ),
    )
    autocomplete_fields = ["instagram_business_account"]
    actions = [fetch_and_save_pages]
