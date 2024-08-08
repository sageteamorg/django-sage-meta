from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class FacebookPageData(AdditionalDataMixin):
    """Model representing Facebook page data.

    Attributes:
        page_id (str): The unique identifier for the Facebook page.
        name (str): The name of the Facebook page.
        category (str): The category of the Facebook page.
        access_token (str): The access token for the Facebook page.
        category_list (list): The list of categories for the Facebook page.
        tasks (list): The list of tasks for the Facebook page.
        instagram_business_account (InstagramAccount): The Instagram business account associated with the Facebook page.

    """

    page_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Page ID"),
        help_text=_("Unique identifier for the Facebook page"),
        db_comment="Primary key for the Facebook page",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the Facebook page"),
        db_comment="The name of the Facebook page",
    )
    category = models.CharField(
        max_length=255,
        verbose_name=_("Category"),
        help_text=_("Category of the Facebook page"),
        db_comment="The category to which the Facebook page belongs",
    )
    access_token = models.CharField(
        max_length=255,
        verbose_name=_("Access Token"),
        help_text=_("Access token for the Facebook page"),
        db_comment="The token used to access the Facebook page API",
    )
    categories = models.ForeignKey(
        "Category",
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Category List"),
        help_text=_("List of categories for the Facebook page"),
        db_comment="Categories associated with the Facebook page",
        related_name="facebook_pages",
    )
    tasks = models.JSONField(
        default=list,
        blank=True,
        verbose_name=_("Tasks"),
        help_text=_("List of tasks for the Facebook page"),
        db_comment="Tasks that can be performed on the Facebook page",
    )
    instagram_business_account = models.OneToOneField(
        "InstagramAccount",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Instagram Business Account"),
        help_text=_("Instagram business account associated with the Facebook page"),
        db_comment="The Instagram business account linked to this Facebook page",
        related_name="facebook_page",
    )

    def __repr__(self):
        return f"<FacebookPageData(page_id={self.page_id}, name={self.name})>"

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("facebook pagedata")
        verbose_name_plural = _("facebook pagedatas")