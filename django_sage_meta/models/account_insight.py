from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class AccountInsight(AdditionalDataMixin):
    """Model representing an account insight.

    Attributes:
        account_insight_id (str): The unique identifier for the account insight.
        name (str): The name of the account insight.
        period (str): The period of the account insight.
        values (list): The list of values for the account insight.
        title (str): The title of the account insight.
        description (str): The description of the account insight.

    """

    account_insight_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Account Insight ID"),
        help_text=_("Unique identifier for the account insight"),
        db_comment="Primary key for the account insight",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the account insight"),
        db_comment="The name of the account insight",
    )
    period = models.CharField(
        max_length=255,
        verbose_name=_("Period"),
        help_text=_("Period of the account insight"),
        db_comment="The period covered by the account insight",
    )
    values = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Values"),
        help_text=_("List of values for the account insight"),
        db_comment="The data values associated with the account insight",
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Title"),
        help_text=_("Title of the account insight"),
        db_comment="The title or headline of the account insight",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name=_("Description"),
        help_text=_("Description of the account insight"),
        db_comment="A detailed description of the account insight",
    )

    def __repr__(self):
        return f"<AccountInsight(account_insight_id={self.account_insight_id}, name={self.name}, period={self.period})>"

    def __str__(self):
        return self.name
