import logging
from django.conf import settings
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


def puth_story(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
    print(queryset)
    client.account_handler.get_accounts()
    for obj in queryset:
        client.content_publisher.publish_story(
            obj.file_url,
        )


puth_story.short_description = "Fetch and Save stories from Facebook"
