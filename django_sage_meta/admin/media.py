from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect


from django_sage_meta.models import Media, Comment
from django_sage_meta.repository import SyncService, PublisherService


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ("comment_id", "text", "username", "like_counts", "timestamp")
    readonly_fields = ("comment_id",)


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        "id",
        "media_id",
        "caption",
        "kind",
        "like_counts",
        "comments_counts",
        "username",
    )
    change_list_template = "admin/email/media.html"
    search_fields = ("media_id", "caption", "kind")
    search_help_text = _("Search by Media ID, Caption, or Media Type")
    list_filter = ("kind", "like_counts", "comments_counts")
    ordering = ("id",)
    inlines = [CommentInline]

    def get_urls(self):
        """Returns the URLs used by this admin.

        This method adds a custom URL for synchronizing media.

        Returns:
            list: A list of URL patterns.

        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-medias/",
                self.admin_site.admin_view(self.sync_media),
                name="sync_media",
            )
        ]
        return custom_urls + urls

    def get_fieldsets(self, request, obj=None):
        """Returns the fieldsets for the admin form.

        For new objects, it returns a custom fieldset with the 'media_url', 'caption', 'kind', and 'carousel' fields.
        For existing objects, it returns the default fieldsets.

        Args:
            request (HttpRequest): The current request object.
            obj (Media, optional): The current media object. Defaults to None.

        Returns:
            list: A list of fieldsets.

        """
        if obj is None:
            return [
                (None, {"fields": ("media_url", "caption", "kind", "carousel")}),
            ]
        return super().get_fieldsets(request, obj)

    def sync_media(self, request):
        """Synchronizes media by calling the SyncService.

        This method attempts to synchronize media and returns an appropriate HttpResponse.

        Args:
            request (HttpRequest): The current request object.

        Returns:
            HttpResponse: An HttpResponse indicating success or failure.

        """
        try:
            SyncService.sync_media()
            self.message_user(request, _("Instagram medias synchronized successfully."))
            change_list_url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
            )
            return redirect(change_list_url)
        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")

    def save_model(self, request, obj, form, change):
        """Saves the model and publishes the media using the PublisherService.

        This method attempts to publish the media and displays a success or error message
        based on the outcome.

        Args:
            request (HttpRequest): The current request object.
            obj (Media): The media object being saved.
            form (ModelForm): The form instance being used.
            change (bool): A flag indicating whether the object is being changed or added.

        """
        media_url = form.cleaned_data.get("media_url")
        caption = form.cleaned_data.get("caption")
        kind = form.cleaned_data.get("kind")
        carousel = form.cleaned_data.get("carousel")

        service = PublisherService()
        try:
            service.publish_media(obj)
            self.message_user(
                request,
                _(
                    "Media published successfully with media_url: {}, caption: {}, kind: {}, carousel: {}"
                ).format(media_url, caption, kind, carousel),
            )
        except Exception as e:
            self.message_user(
                request,
                _(f"An error occurred while publishing media: {e}"),
                level="error",
            )
        return
