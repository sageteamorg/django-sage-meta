import logging
from django.conf import settings
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


def puth_comment(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
    print(queryset)
    client.account_handler.get_accounts()
    for obj in queryset:
        client.content_publisher.put_comment(obj.media.media_id, obj.caption)


puth_comment.short_description = "puth and Save comment from Facebook"
