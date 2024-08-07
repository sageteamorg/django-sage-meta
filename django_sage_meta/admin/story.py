from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("id", "story_id", "media_type", "media_url", "timestamp")
    search_fields = ("story_id", "media_type", "media_url")
    search_help_text = _("Search by Story ID, Media Type, or Media URL")
    list_filter = ("media_type", "timestamp")
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("story_id", "media_type", "media_url", "timestamp")}),
    )
