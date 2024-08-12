from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.http import HttpResponseRedirect

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
            return HttpResponseRedirect(
                "http://127.0.0.1:8000/admin/django_sage_meta/category/"
            )

        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
