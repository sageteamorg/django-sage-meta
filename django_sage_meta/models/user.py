from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class UserData(AdditionalDataMixin):
    """
    Model representing user data.

    Attributes```python
        user_id (str): The unique identifier for the user.
        name (str): The name of the user.
        email (str): The email of the user.
        pages (list): The list of Facebook pages associated with the user.
    """

    user_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("User ID"),
        help_text=_("Unique identifier for the user"),
        db_comment="Primary key for the user",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the user"),
        db_comment="The full name of the user",
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_("Email"),
        help_text=_("Email of the user"),
        db_comment="The email address of the user",
    )
    pages = models.OneToOneField(
        "FacebookPageData",
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Pages"),
        help_text=_("List of Facebook pages associated with the user"),
        db_comment="Facebook pages linked to this user",
        related_name="users",
    )

    def __repr__(self):
        return f"<UserData(user_id={self.user_id}, name={self.name})>"

    def __str__(self):
        return self.name
