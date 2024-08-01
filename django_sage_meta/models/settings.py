from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class Settings(AdditionalDataMixin):
    """
    Model representing application settings.

    Attributes:
        access_token (str): The access token for the API.
        business_account_id (str): The ID of the business account.
        user_id (str): The ID of the user.
        messenger_token (str): The token for Messenger API access.
    """

    access_token = models.CharField(
        max_length=255,
        verbose_name=_("Access Token"),
        help_text=_("Access token for the API"),
        db_comment="The access token used for authenticating API requests",
    )
    business_account_id = models.CharField(
        max_length=255,
        verbose_name=_("Business Account ID"),
        help_text=_("ID of the business account"),
        db_comment="The unique identifier for the business account",
    )
    user_id = models.CharField(
        max_length=255,
        verbose_name=_("User ID"),
        help_text=_("ID of the user"),
        db_comment="The unique identifier for the user",
    )
    messenger_token = models.CharField(
        max_length=255,
        verbose_name=_("Messenger Token"),
        help_text=_("Token for Messenger API access"),
        db_comment="The token used for accessing the Messenger API",
    )

    def __repr__(self):
        return f"<Settings(access_token={self.access_token}, business_account_id={self.business_account_id}, user_id={self.user_id})>"

    def __str__(self):
        return self.business_account_id
