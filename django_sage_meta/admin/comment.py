from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from ..models import Comment
from ..resources import CommentResource


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentResource
    save_on_top = True
    list_display = ("id", "comment_id", "username", "like_count", "timestamp")
    search_fields = ("comment_id", "username", "text")
    search_help_text = _("Search by Comment ID, Username, or Text")
    list_filter = ("like_count", "timestamp")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {"fields": ("comment_id", "text", "username", "like_count", "timestamp")},
        ),
    )
