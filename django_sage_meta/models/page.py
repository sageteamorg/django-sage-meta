from django.db import models
from django.utils.translation import gettext_lazy as _

from django_sage_meta.helper.mixins import AdditionalDataMixin


class FacebookPageData(AdditionalDataMixin):
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
        help_text=_("Access token for the Facebook page"),
        db_comment="The token used to access the Facebook page API",
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
        related_name="facebook_page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Instagram business account associated with the Facebook page"),
        db_comment="The Instagram business account linked to this Facebook page",
    )
    category = models.ForeignKey(
        "Category",
        verbose_name=_("Category List"),
        related_name="facebook_pages",
        blank=True,
        on_delete=models.CASCADE,
        help_text=_("List of categories for the Facebook page"),
        db_comment="Categories associated with the Facebook page",
    )
    user = models.OneToOneField(
        "UserData",
        verbose_name=_("users"),
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
        verbose_name = _("Facebook Pagedata")
        verbose_name_plural = _("Facebook Pagedatas")
