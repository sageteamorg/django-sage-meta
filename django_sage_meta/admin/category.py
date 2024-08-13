from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect

from django_sage_meta.repository import SyncService
from django_sage_meta.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/category.html"

    list_display = ("id", "category_id", "name")
    search_fields = ("category_id", "name")
    search_help_text = _("Search by Category ID or Name")
    ordering = ("id",)
    fieldsets = (("Content", {"fields": ("category_id", "name")}),)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-cats/",
                self.admin_site.admin_view(self.sync_categories),
                name="sync_cats",
            )
        ]
        return custom_urls + urls

    def sync_categories(self, request):
        try:
            SyncService.sync_categories()
            self.message_user(
                request, _("Instagram categories synchronized successfully.")
            )
            change_list_url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
            )
            return redirect(change_list_url)

        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
