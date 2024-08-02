from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class Story(AdditionalDataMixin):
    """Model representing a story.

    Attributes:
        story_id (str): The unique identifier for the story.
        media_type (str): The type of media in the story.
        media_url (str): The URL of the media in the story.
        timestamp (str): The timestamp of the story.

    """

    story_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Story ID"),
        help_text=_("Unique identifier for the story"),
        db_comment="Primary key for the story",
    )
    media_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Media Type"),
        help_text=_("Type of media content in the story"),
        db_comment="The media type of the story (e.g., image, video)",
    )
    media_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Media URL"),
        help_text=_("URL of the media content"),
        db_comment="The URL where the media is stored",
    )
    timestamp = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Timestamp"),
        help_text=_("When the story was created"),
        db_comment="Timestamp indicating when the story was created",
    )

    def __repr__(self):
        return f"<Story(story_id={self.story_id}, media_type={self.media_type}, media_url={self.media_url})>"

    def __str__(self):
        return self.story_id
