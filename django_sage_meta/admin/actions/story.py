import logging
from django.conf import settings
from django.db import IntegrityError
from django_sage_meta.models import Story
from sage_meta.service import FacebookClient

logger = logging.getLogger(__name__)


def fetch_and_save_stories(modeladmin, request, queryset):
    client = FacebookClient(settings.FACEBOOK_ACCESS_TOKEN)

    try:
        stories = client.story_handler.get_instagram_stories(settings.INSTA_ID)

        story_objs = [
            Story(
                story_id=story.id,
                media_type=story.media_type,
                media_url=story.media_url,
                timestamp=story.timestamp,
            )
            for story in stories
        ]

        Story.objects.bulk_create(story_objs, ignore_conflicts=True)
        modeladmin.message_user(
            request, "Stories have been fetched and saved successfully."
        )
    except IntegrityError as e:
        modeladmin.message_user(
            request, f"Database integrity error: {e}", level="error"
        )
    except Exception as e:
        modeladmin.message_user(
            request, f"Error fetching and saving stories: {e}", level="error"
        )


fetch_and_save_stories.short_description = "Fetch and Save Stories from Facebook"
