from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django_sage_meta.models import Category
from django_sage_meta.admin.actions import fetch_and_save_categories


@admin.register(Category)
class CategoryAdmin:
    save_on_top = True
    list_display = ("id", "category_id", "name")
    search_fields = ("category_id", "name")
    search_help_text = _("Search by Category ID or Name")
    ordering = ("id",)
    fieldsets = (("Content", {"fields": ("category_id", "name")}),)
    actions = [fetch_and_save_categories]

    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('sync-values/', self.admin_site.admin_view(self.sync_values), name='sync_values'),
    #     ]
    #     return custom_urls + urls

    # def sync_values(self, request):
    #     self.message_user(request, "Values have been synced.")
    #     return HttpResponseRedirect(reverse('admin:django_sage_meta_category_changelist'))

    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['sync_values_url'] = reverse('admin:sync_values')
    #     return super().changelist_view(request, extra_context=extra_context)
