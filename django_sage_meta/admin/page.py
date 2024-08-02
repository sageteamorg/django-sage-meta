from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import FacebookPageData


@admin.register(FacebookPageData)
class FacebookPageDataAdmin(admin.ModelAdmin):
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
