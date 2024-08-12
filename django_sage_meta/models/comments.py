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
        verbose_name=_("Comment ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the comment"),
        db_comment="Primary key for the comment",
    )
    text = models.TextField(
        verbose_name=_("Text"),
        null=True,
        blank=True,
        help_text=_("Text of the comment"),
        db_comment="The content of the comment",
    )
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Username of the commenter"),
        db_comment="The username of the person who made the comment",
    )
    like_counts = models.IntegerField(
        verbose_name=_("Like Counts"),
        null=True,
        blank=True,
        help_text=_("Number of likes on the comment"),
        db_comment="The total number of likes the comment has received",
    )
    timestamp = models.CharField(
        verbose_name=_("Timestamp"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Timestamp of the comment"),
        db_comment="Timestamp indicating when the comment was made",
    )
    media = models.ForeignKey(
        "Media",
        verbose_name=_("Media"),
        related_name="comments",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("The media this comment is associated with"),
        db_comment="The media this comment is associated with",
    )

    def __repr__(self):
        return f"<Comment(comment_id={self.comment_id}, username={self.username}, text={self.text})>"

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
