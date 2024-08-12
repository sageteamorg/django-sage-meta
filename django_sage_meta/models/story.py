from django.db import models
from django.utils.translation import gettext_lazy as _

from django_sage_meta.helper.mixins import AdditionalDataMixin


class Story(AdditionalDataMixin):
    story_id = models.CharField(
        _("Story ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the story"),
        db_comment="Primary key for the story",
    )
    media_type = models.CharField(
        _("Media Type"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Type of media content in the story"),
        db_comment="The media type of the story (e.g., image, video)",
    )
    media_url = models.CharField(
        _("Media URL"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("URL of the media content"),
        db_comment="The URL where the media is stored",
    )
    timestamp = models.CharField(
        _("Timestamp"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("When the story was created"),
        db_comment="Timestamp indicating when the story was created",
    )
    account = models.ForeignKey(
        "InstagramAccount",
        verbose_name=_("Instagram Story User"),
        related_name="stories",
        on_delete=models.CASCADE,
        blank=True,
        help_text=_("List of stories posted by this account"),
        db_comment="Stories posted by this Instagram account",
    )

    def __repr__(self):
        return f"<Story(story_id={self.story_id}, media_type={self.media_type}, media_url={self.media_url})>"

    def __str__(self):
        return self.story_id

    class Meta:
        verbose_name = _("Story")
        verbose_name_plural = _("Stories")
