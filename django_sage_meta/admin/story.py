from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django_sage_meta.models import Story
from django_sage_meta.repository import SyncService
from django_sage_meta.repository import PublisherService
from django.http import HttpResponse

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
        try:
            SyncService.sync_stories()
            self.message_user(request, _("Instagram accounts synchronized successfully."))
            return HttpResponse("Sync completed successfully.")

        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level='error')

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return [
                (None, {
                    'fields': ('media_url', 'user')
                }),
            ]
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        media_url = form.cleaned_data.get('media_url')

        service = PublisherService()
        try:
            service.publish_story(obj)
            self.message_user(request, _("Story published successfully with media_url: {}").format(media_url))
        except Exception as e:
            self.message_user(request, _(f"An error occurred while publishing story: {e}"), level='error')

        return
