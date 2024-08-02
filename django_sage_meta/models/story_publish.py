from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from ..helper.choice import ContentFileEnum


class StoryPublisher(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE
    )

    file_url = models.CharField(max_length=255)

    kind = models.CharField(
        choices=ContentFileEnum.choices,
        max_length=10,
        verbose_name=_("kind"),
    )

    class Meta:
        verbose_name = _("story_publisher")
        verbose_name_plural = _("story_publishers")
