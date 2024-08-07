from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django_sage_meta.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
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
