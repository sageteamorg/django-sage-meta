import logging
from django.conf import settings
from django_sage_meta.models import Media, Comment
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)

def fetch_and_save_media(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)
    
    media_list = client.media_handler.get_instagram_media(settings.INSTA_ID)
        
    media_objs = []
    all_comment_objs = []
    media_to_comments = []

    for media in media_list:
        comment_objs = []
        comments = client.comment_handler.get_instagram_comments(media.id)

        for comment in comments:
            comment_obj = Comment(
                comment_id=comment.id,
                text=comment.text,
                username=comment.username,
                like_count=comment.like_count,
                timestamp=comment.timestamp,
            )
            comment_objs.append(comment_obj)
            all_comment_objs.append(comment_obj)
        
        media_obj = Media(
            media_id=media.id,
            caption=media.caption,
            media_type=media.media_type,
            media_url=media.media_url,
            timestamp=media.timestamp,
            like_count=media.like_count,
            comments_count=media.comments_count,
            username=media.username,
        )
        media_objs.append(media_obj)
        media_to_comments.append((media.id, comment_objs))

    Media.objects.bulk_create(media_objs, ignore_conflicts=True)
    Comment.objects.bulk_create(all_comment_objs, ignore_conflicts=True)

    for media_id, comments in media_to_comments:
        media_obj = Media.objects.get(media_id=media_id)
        comment_objs = Comment.objects.filter(comment_id__in=[comment.comment_id for comment in comments])
        media_obj.comments.set(comment_objs)

    modeladmin.message_user(request, "Media and comments have been fetched and saved successfully.")

fetch_and_save_media.short_description = "Fetch and Save Media from Facebook"

