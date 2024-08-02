from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django_sage_meta.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("id", "category_id", "name")
    search_fields = ("category_id", "name")
    search_help_text = _("Search by Category ID or Name")
    ordering = ("id",)
    fieldsets = (("Content", {"fields": ("category_id", "name")}),)
