from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django_sage_meta.models import Comment
from django_sage_meta.repository import PublisherService


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("id", "comment_id", "username", "like_counts", "timestamp", "media")
    search_fields = ("comment_id", "username", "text")
    search_help_text = _("Search by Comment ID, Username, or Text")
    list_filter = ("like_counts", "timestamp")
    ordering = ("id",)
    fieldsets = (
        (
            "Content",
            {"fields": ("comment_id", "text", "username", "like_counts", "timestamp")},
        ),
    )
    autocomplete_fields = ["media"]

    def get_fieldsets(self, request, obj=None):
        """Returns the fieldsets for the admin form.

        For new objects, it returns a custom fieldset with the 'media' and 'text' fields.
        For existing objects, it returns the default fieldsets.

        Args:
            request (HttpRequest): The current request object.
            obj (Comment, optional): The current comment object. Defaults to None.

        Returns:
            list: A list of fieldsets.

        """
        if obj is None:
            return [
                (
                    None,
                    {
                        "fields": (
                            "media",
                            "text",
                        )
                    },
                ),
            ]
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """Saves the model and publishes the comment using the
        PublisherService.

        This method attempts to publish the comment and displays a success or error message
        based on the outcome.

        Args:
            request (HttpRequest): The current request object.
            obj (Comment): The comment object being saved.
            form (ModelForm): The form instance being used.
            change (bool): A flag indicating whether the object is being changed or added.

        """
        service = PublisherService()
        try:
            service.publish_comment(obj)
            self.message_user(
                request,
                _("Comment published successfully with comment_id: {}").format(
                    obj.comment_id
                ),
            )
        except Exception as e:
            self.message_user(
                request,
                _(f"An error occurred while publishing comment: {e}"),
                level="error",
            )
        return
