from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect

from django_sage_meta.models import UserData
from django_sage_meta.repository import SyncService


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    save_on_top = True
    change_list_template = "admin/email/user.html"
    list_display = ("id", "user_id", "name", "email")
    search_fields = ("user_id", "name", "email")
    search_help_text = _("Search by User ID, Name, or Email")
    list_filter = ("email",)
    ordering = ("id",)
    fieldsets = (("Content", {"fields": ("user_id", "name", "email")}),)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-users/",
                self.admin_site.admin_view(self.sync_insta_user),
                name="sync_users",
            )
        ]
        return custom_urls + urls

    def sync_insta_user(self, request):
        try:
            SyncService.sync_user_data()
            self.message_user(request, _("Instagram users synchronized successfully."))
            change_list_url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
            )
            return redirect(change_list_url)
        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")
