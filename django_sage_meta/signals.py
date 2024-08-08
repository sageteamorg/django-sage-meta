from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django_sage_meta.models import Media
from sage_meta.service import FacebookClient
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Media)
def publish_to_instagram(sender, instance, created, **kwargs):
    if created:
        client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
        client.account_handler.get_accounts()
        
        if instance.kind == 'image':
            if instance.carousel:
                carousel_list = instance.media_url.split(',')
                client.content_publisher.publish_carousel(
                    carousel_list,
                    instance.caption
                )
            else:
                client.content_publisher.publish_photo(
                    instance.media_url,
                    instance.caption
                )
        elif instance.kind == 'video':
            client.content_publisher.publish_video(
                instance.media_url,
                instance.caption
            )
