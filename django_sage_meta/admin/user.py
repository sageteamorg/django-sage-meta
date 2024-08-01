from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from django_sage_meta.models import UserData
from django_sage_meta.resources import UserDataResource
from django_sage_meta.admin.actions.user import fetch_and_save_user_data

@admin.register(UserData)
class UserDataAdmin(ImportExportModelAdmin):
    resource_class = UserDataResource
    save_on_top = True
    list_display = ("id", "user_id", "name", "email")
    search_fields = ("user_id", "name", "email")
    search_help_text = _("Search by User ID, Name, or Email")
    list_filter = ("email",)
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("user_id", "name", "email")}),
        ("Pages", {"fields": ("pages",), "classes": ("collapse",)}),
    )
    actions = [fetch_and_save_user_data]