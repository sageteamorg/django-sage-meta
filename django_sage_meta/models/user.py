from django.db import models
from django.utils.translation import gettext_lazy as _

from django_sage_meta.helper.mixins import AdditionalDataMixin


class UserData(AdditionalDataMixin):
    """
    Represents a user within the system, storing key information such as the user's unique identifier,
    name, and email address. This model serves as the central point of user-related data management 
    in the application.

    The `UserData` model is designed to facilitate the synchronization and management of user data 
    from external services, ensuring that the application has up-to-date information about each user.

    """
    user_id = models.CharField(
        _("User ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the user"),
        db_comment="Primary key for the user",
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name of the user"),
        db_comment="The full name of the user",
    )
    email = models.EmailField(
        _("Email"),
        null=True,
        blank=True,
        help_text=_("Email of the user"),
        db_comment="The email address of the user",
    )

    def __repr__(self):
        return f"<UserData(user_id={self.user_id}, name={self.name})>"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("User data")
        verbose_name_plural = _("User datas")
