import logging
from django.conf import settings
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


def puth_post(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
    print(queryset)
    client.account_handler.get_accounts()
    for obj in queryset:
        if obj.kind == "post":
            if obj.carousel:
                carousel_list = obj.file_url.split(",")

                client.content_publisher.publish_carousel(carousel_list, obj.caption)

            else:
                client.content_publisher.publish_photo(obj.file_url, obj.caption)
        else:
            client.content_publisher.publish_video()


puth_post.short_description = "Fetch and Save Pages from Facebook"
