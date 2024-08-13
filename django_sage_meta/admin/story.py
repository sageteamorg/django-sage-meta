from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect

from django_sage_meta.models import Story
from django_sage_meta.repository import SyncService, PublisherService


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    change_list_template = "admin/email/story.html"
    save_on_top = True
    list_display = ("id", "story_id", "media_type", "media_url", "timestamp")
    search_fields = ("story_id", "media_type", "media_url")
    search_help_text = _("Search by Story ID, Media Type, or Media URL")
    list_filter = ("media_type", "timestamp")
    ordering = ("id",)
    fieldsets = (
        ("Content", {"fields": ("story_id", "media_type", "media_url", "timestamp")}),
    )

    def get_urls(self):
        """Returns the URLs used by this admin.

        This method adds a custom URL for synchronizing stories.

        Returns:
            list: A list of URL patterns.

        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "sync-items/",
                self.admin_site.admin_view(self.sync_insta_story),
                name="sync_items",
            )
        ]
        return custom_urls + urls

    def sync_insta_story(self, request):
        """Synchronizes stories by calling the SyncService.

        This method attempts to synchronize stories and returns an appropriate HttpResponse.

        Args:
            request (HttpRequest): The current request object.

        Returns:
            HttpResponse: An HttpResponse indicating success or failure.

        """
        try:
            SyncService.sync_stories()
            self.message_user(
                request, _("Instagram accounts synchronized successfully.")
            )
            change_list_url = reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist"
            )
            return redirect(change_list_url)
        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level="error")

    def get_fieldsets(self, request, obj=None):
        """Returns the fieldsets for the admin form.

        For new objects, it returns a custom fieldset with the 'media_url' and 'user' fields.
        For existing objects, it returns the default fieldsets.

        Args:
            request (HttpRequest): The current request object.
            obj (Story, optional): The current story object. Defaults to None.

        Returns:
            list: A list of fieldsets.

        """
        if obj is None:
            return [
                (None, {"fields": ("media_url",)}),
            ]
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """Saves the model and publishes the story using the PublisherService.

        This method attempts to publish the story and displays a success or error message
        based on the outcome.

        Args:
            request (HttpRequest): The current request object.
            obj (Story): The story object being saved.
            form (ModelForm): The form instance being used.
            change (bool): A flag indicating whether the object is being changed or added.

        """
        media_url = form.cleaned_data.get("media_url")

        service = PublisherService()
        try:
            service.publish_story(obj)
            self.message_user(
                request,
                _("Story published successfully with media_url: {}").format(media_url),
            )
        except Exception as e:
            self.message_user(
                request,
                _(f"An error occurred while publishing story: {e}"),
                level="error",
            )

        return
