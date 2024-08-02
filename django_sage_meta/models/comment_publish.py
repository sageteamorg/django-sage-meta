from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CommentPublisher(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )

    media = models.ForeignKey(
        "Media",
        related_name="media_comment",
        verbose_name=_("media_comment"),
        help_text=_("Which media is for this comment"),
        on_delete=models.CASCADE,
    )

    caption = models.TextField()
    replay = models.ForeignKey(
        "self",
        verbose_name=_("replay"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Comment_Publish")
        verbose_name_plural = _("Comment_Publishs")
