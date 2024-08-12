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
        verbose_name=_("Insight ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the insight"),
        db_comment="Primary key for the insight",
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        help_text=_("Name of the insight"),
        db_comment="The name of the insight",
    )
    period = models.CharField(
        verbose_name=_("Period"),
        max_length=255,
        help_text=_("Period of the insight"),
        db_comment="The period covered by the insight",
    )
    values = models.JSONField(
        verbose_name=_("Values"),
        default=list,
        blank=True,
        help_text=_("List of values for the insight"),
        db_comment="The data values associated with the insight",
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Title of the insight"),
        db_comment="The title or headline of the insight",
    )
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Description of the insight"),
        db_comment="A detailed description of the insight",
    )
    account = models.ForeignKey(
        "InstagramAccount",
        verbose_name=_("account"),
        related_name="insights",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text=_("List of insights for this account"),
        db_comment="Insights related to the Instagram account",
    )
    def __repr__(self):
        return f"<Insight(insight_id={self.insight_id}, name={self.name}, period={self.period})>"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Insight")
        verbose_name_plural = _("Insights")
