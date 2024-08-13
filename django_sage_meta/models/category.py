from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class Category(AdditionalDataMixin):
    """Model representing a category.

    Attributes:
        category_id (str): The unique identifier for the category.
        name (str): The name of the category.

    """

    category_id = models.CharField(
        verbose_name=_("Category ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the category"),
        db_comment="Primary key for the category",
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        help_text=_("Name of the category"),
        db_comment="The name of the category",
    )

    def __repr__(self):
        return f"<Category(category_id={self.category_id}, name={self.name})>"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
