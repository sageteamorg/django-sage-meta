from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin

from django_sage_meta.helper.choice import ContentFileEnum


class Media(AdditionalDataMixin):
    media_id = models.CharField(
        _("Media ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the media"),
        db_comment="Primary key for the media",
    )
    username = models.CharField(
        _("Username"),
        max_length=255,
        help_text=_("Username of the account"),
        db_comment="The handle or username of the Instagram account",
    )
    caption = models.TextField(
        _("Caption"),
        null=True,
        blank=True,
        help_text=_("Caption for the media"),
        db_comment="The caption or description of the media content",
    )
    media_url = models.TextField(
        _("Media URLs"),
        blank=True,
        help_text=_("URLs for the media content"),
        db_comment="List of URLs where the media files are stored",
    )
    timestamp = models.CharField(
        _("Timestamp"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("When the media was created or published"),
        db_comment="Timestamp indicating when the media content was created or published",
    )
    like_counts = models.IntegerField(
        _("Like Counts"),
        null=True,
        blank=True,
        help_text=_("Number of likes on the media"),
        db_comment="The total number of likes the media has received",
    )
    comments_counts = models.IntegerField(
        _("Comments Counts"),
        null=True,
        blank=True,
        help_text=_("Number of comments on the media"),
        db_comment="The total number of comments on the media",
    )
    kind = models.CharField(
        _("Kind"),
        choices=ContentFileEnum.choices,
        max_length=10,
        null=True,
        blank=True,
        help_text=_("Media kind"),
        db_comment="What kind of media is saving in db",
    )
    carousel = models.BooleanField(
        _("Carousel"),
        default=False,
        help_text=_("Is this media a gallery"),
        db_comment="Media is a gallery",
    )
    account = models.ForeignKey(
        "InstagramAccount",
        verbose_name=_("Instagram account"),
        related_name="medias",
        on_delete=models.CASCADE,
        blank=True,
        help_text=_("List of medias posted by this account"),
        db_comment="Medias posted by this Instagram account",
    )

    def __repr__(self):
        return f"<Media(media_id={self.media_id}, caption={self.caption}, media_type={self.media_type})>"

    def __str__(self):
        return self.caption or ""

    class Meta:
        verbose_name = _("media")
        verbose_name_plural = _("medias")
