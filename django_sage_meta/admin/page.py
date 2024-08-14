from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect

from django_sage_meta.models import FacebookPageData
from django_sage_meta.repository import SyncService


@admin.register(FacebookPageData)
class FacebookPageDataAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/page.html"

    list_display = ("page_id", "name")
    search_fields = ("page_id", "name", "categories")
    search_help_text = _("Search by Page ID, Name, or Category")
    list_filter = ("categories",)
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("page_id", "name", "access_token")}),
        (
            "Tasks",
            {"fields": ("tasks",), "classes": ("collapse",)},
        ),
        (
            "Instagram Business Account",
            {"fields": ("instagram_business_account",), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("access_token",)
    autocomplete_fields = ("instagram_business_account",)
    filter_horizontal = ("categories",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-page/",
                self.admin_site.admin_view(self.sync_insta_page),
                name="sync_page",
            )
        ]
        return custom_urls + urls

    def sync_insta_page(self, request):
        SyncService.sync_facebook_pages()
        self.message_user(request, _("Instagram pages synchronized successfully."))
        change_list_url = reverse(
            f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
        )
        return redirect(change_list_url)
