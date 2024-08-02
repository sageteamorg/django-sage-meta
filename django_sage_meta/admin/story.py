from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from django_sage_meta.models import Story
from django_sage_meta.resources import StoryResource
from django_sage_meta.admin.actions.story import fetch_and_save_stories


@admin.register(Story)
class StoryAdmin(ImportExportModelAdmin):
    resource_class = StoryResource
    save_on_top = True
    list_display = ("id", "story_id", "media_type", "media_url", "timestamp")
    search_fields = ("story_id", "media_type", "media_url")
    search_help_text = _("Search by Story ID, Media Type, or Media URL")
    list_filter = ("media_type", "timestamp")
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("story_id", "media_type", "media_url", "timestamp")}),
    )
    actions = [fetch_and_save_stories]
