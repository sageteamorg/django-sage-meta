from django.db import models
from django.utils.translation import gettext_lazy as _


class AdditionalDataMixin(models.Model):
    """Mixin representing additional data.

    Attributes:
        additional_data (dict): Any extra information that is not captured by other fields.

    """

    additional_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Additional Data"),
        help_text=_("Any extra information that is not captured by other fields."),
        db_comment="Any extra information that is not captured by other fields.",
    )

    class Meta:
        abstract = True
