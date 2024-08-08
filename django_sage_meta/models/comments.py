from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class Comment(AdditionalDataMixin):
    """Model representing a comment.

    Attributes:
        comment_id (str): The unique identifier for the comment.
        text (str): The text of the comment.
        username (str): The username of the commenter.
        like_count (int): The number of likes on the comment.
        timestamp (str): The timestamp of the comment.

    """

    comment_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Comment ID"),
        db_comment="Primary key for the comment",
        help_text=_("Unique identifier for the comment"),
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Text"),
        db_comment="The content of the comment",
        help_text=_("Text of the comment"),
    )
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Username"),
        db_comment="The username of the person who made the comment",
        help_text=_("Username of the commenter"),
    )
    like_count = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("Like Count"),
        db_comment="The total number of likes the comment has received",
        help_text=_("Number of likes on the comment"),
    )
    timestamp = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Timestamp"),
        db_comment="Timestamp indicating when the comment was made",
        help_text=_("Timestamp of the comment"),
    )
    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='c_media',
        verbose_name=_("Media"),
        help_text=_("The media this comment is associated with"),
        db_comment="The media this comment is associated with",
    )

    def __repr__(self):
        return f"<Comment(comment_id={self.comment_id}, username={self.username}, text={self.text})>"

    def __str__(self):
        return self.text or ""

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")