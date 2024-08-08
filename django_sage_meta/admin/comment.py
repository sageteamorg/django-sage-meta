# admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_sage_meta.models import Comment
from django_sage_meta.repository import PublisherService

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

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return [
                (None, {
                    'fields': ('media', 'text',)
                }),
            ]
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        service = PublisherService()
        try:
            service.publish_comment(obj)
            self.message_user(request, _("Comment published successfully with comment_id: {}").format(obj.comment_id))
        except Exception as e:
            self.message_user(request, _(f"An error occurred while publishing comment: {e}"), level='error')
        return
