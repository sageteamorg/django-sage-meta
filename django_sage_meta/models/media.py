from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class Media(AdditionalDataMixin):
    """Model representing media content.

    Attributes:
        media_id (str): The unique identifier for the media.
        caption (str): The caption of the media.
        media_type (str): The type of media.
        media_url (list): The list of URLs for the media.
        timestamp (str): The timestamp of the media.
        like_count (int): The number of likes on the media.
        comments_count (int): The number of comments on the media.
        comments (list): The list of comments on the media.

    """

    media_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Media ID"),
        help_text=_("Unique identifier for the media"),
        db_comment="Primary key for the media",
    )
    username = models.CharField(
        max_length=255,
        verbose_name=_("Username"),
        help_text=_("Username of the account"),
        db_comment="The handle or username of the Instagram account",
    )
    caption = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Caption"),
        help_text=_("Caption for the media"),
        db_comment="The caption or description of the media content",
    )
    media_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Media Type"),
        help_text=_("Type of media (e.g., image, video)"),
        db_comment="The format or type of the media content",
    )
    media_url = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Media URLs"),
        help_text=_("URLs for the media content"),
        db_comment="List of URLs where the media files are stored",
    )
    timestamp = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Timestamp"),
        help_text=_("When the media was created or published"),
        db_comment="Timestamp indicating when the media content was created or published",
    )
    like_count = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Like Count"),
        help_text=_("Number of likes on the media"),
        db_comment="The total number of likes the media has received",
    )
    comments_count = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Comments Count"),
        help_text=_("Number of comments on the media"),
        db_comment="The total number of comments on the media",
    )
    comments = models.ManyToManyField(
        "Comment",
        blank=True,
        verbose_name=_("Comments"),
        help_text=_("List of comments on the media"),
        db_comment="Comments related to the media content",
        related_name="media_comments",
    )

    def __repr__(self):
        return f"<Media(media_id={self.media_id}, caption={self.caption}, media_type={self.media_type})>"

    def __str__(self):
        return self.caption or ""
