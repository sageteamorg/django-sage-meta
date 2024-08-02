from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import UserData


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
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

