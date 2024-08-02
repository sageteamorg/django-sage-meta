from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class Insight(AdditionalDataMixin):
    """Model representing an insight.

    Attributes:
        insight_id (str): The unique identifier for the insight.
        name (str): The name of the insight.
        period (str): The period of the insight.
        values (list): The list of values for the insight.
        title (str): The title of the insight.
        description (str): The description of the insight.

    """

    insight_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Insight ID"),
        help_text=_("Unique identifier for the insight"),
        db_comment="Primary key for the insight",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the insight"),
        db_comment="The name of the insight",
    )
    period = models.CharField(
        max_length=255,
        verbose_name=_("Period"),
        help_text=_("Period of the insight"),
        db_comment="The period covered by the insight",
    )
    values = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Values"),
        help_text=_("List of values for the insight"),
        db_comment="The data values associated with the insight",
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Title"),
        help_text=_("Title of the insight"),
        db_comment="The title or headline of the insight",
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Description of the insight"),
        db_comment="A detailed description of the insight",
    )

    def __repr__(self):
        return f"<Insight(insight_id={self.insight_id}, name={self.name}, period={self.period})>"

    def __str__(self):
        return self.name
