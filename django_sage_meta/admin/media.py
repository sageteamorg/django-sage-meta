from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_sage_meta.models import Media
from django.urls import path
from django_sage_meta.repository import SyncService
from django_sage_meta.repository import PublisherService
from django.http import HttpResponse

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        "id",
        "media_id",
        "caption",
        "kind",
        "like_count",
        "comments_count",
        "username",
    )
    change_list_template = "admin/email/media.html"
    search_fields = ("media_id", "caption", "kind")
    search_help_text = _("Search by Media ID, Caption, or Media Type")
    list_filter = ("kind", "like_count", "comments_count")
    ordering = ("id",)
    autocomplete_fields = ["comments"]

    def get_urls(self):
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
        if obj is None:
            return [
                (None, {
                    'fields': ('media_url', 'caption', 'kind', 'carousel')
                }),
            ]
        return super().get_fieldsets(request, obj)

    def sync_media(self, request):
        try:
            SyncService.sync_media()
            self.message_user(request, _("Instagram medias synchronized successfully."))
            return HttpResponse("Sync completed successfully.")

        except Exception as e:
            self.message_user(request, _(f"An error occurred: {e}"), level='error')

    def save_model(self, request, obj, form, change):
        media_url = form.cleaned_data.get('media_url')
        caption = form.cleaned_data.get('caption')
        kind = form.cleaned_data.get('kind')
        carousel = form.cleaned_data.get('carousel')

        service = PublisherService()
        try:
            service.publish_media(obj)
            self.message_user(request, _("Media published successfully with media_url: {}, caption: {}, kind: {}, carousel: {}").format(media_url, caption, kind, carousel))
        except Exception as e:
            self.message_user(request, _(f"An error occurred while publishing media: {e}"), level='error')
        return
