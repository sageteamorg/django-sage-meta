from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from django_sage_meta.helper.mixins import AdditionalDataMixin


class FacebookPageData(AdditionalDataMixin):
    """Represents a Facebook page within the application, capturing its core
    details and related associations. This model is designed to store key
    information such as the unique identifier for the page, its name, and the
    access token necessary for interacting with Facebook's API.

    Additionally, the model supports relationships to other entities,
    such as categories, users, and Instagram business accounts, allowing
    for a comprehensive representation of the Facebook page within the
    system.

    The data stored in this model is primarily used for synchronization
    processes between Facebook and the local database, facilitated by
    service classes like SyncService. These processes ensure that the
    application's representation of Facebook pages remains up-to-date
    with the latest information available via Facebook's APIs.

    """

    page_id = models.CharField(
        _("Page ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the Facebook page"),
        db_comment="Primary key for the Facebook page",
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("Name of the Facebook page"),
        db_comment="The name of the Facebook page",
    )
    access_token = models.CharField(
        _("Access Token"),
        max_length=255,
        help_text=_(
            "Access token for the Facebook page for access the graph api endpoint"
        ),
        db_comment="The token used to access the Facebook page API and without it we can not access the to database",
    )
    tasks = models.JSONField(
        _("Tasks"),
        default=list,
        blank=True,
        help_text=_("List of tasks for the Facebook page"),
        db_comment="Tasks that can be performed on the Facebook page",
    )
    instagram_business_account = models.OneToOneField(
        "InstagramAccount",
        verbose_name=_("Instagram Business Account"),
        related_name="page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Instagram business account associated with the Facebook page"),
        db_comment="The Instagram business account linked to this Facebook page",
    )
    categories = models.ManyToManyField(
        "Category",
        verbose_name=_("Category List"),
        related_name="pages",
        blank=True,
        help_text=_("List of categories for the Facebook page"),
        db_comment="Categories associated with the Facebook page",
    )
    user = models.OneToOneField(
        "UserData",
        verbose_name=_("user"),
        related_name="page",
        blank=True,
        on_delete=models.CASCADE,
        help_text=_("user associated with this page"),
        db_comment="user linked to this page",
    )

    def __repr__(self):
        return f"<FacebookPageData(page_id={self.page_id}, name={self.name})>"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Facebook Page Data")
        verbose_name_plural = _("Facebook Page Datas")
