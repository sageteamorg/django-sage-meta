from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class InstagramAccount(AdditionalDataMixin):
    account_id = models.CharField(
        _("Account ID"),
        max_length=255,
        unique=True,
        help_text=_("Unique identifier for the account"),
        db_comment="Primary key for the Instagram account",
    )
    username = models.CharField(
        _("Username"),
        max_length=255,
        help_text=_("Username of the account"),
        db_comment="The handle or username of the Instagram account",
    )
    follows_counts = models.IntegerField(
        _("Follows Counts"),
        help_text=_("Number of accounts this account follows"),
        db_comment="The total number of accounts followed by this Instagram account",
    )
    followers_counts = models.IntegerField(
        _("Followers Count"),
        help_text=_("Number of followers of this account"),
        db_comment="The total number of followers of this Instagram account",
    )
    media_counts = models.IntegerField(
        _("Media Counts"),
        help_text=_("Number of media items posted by this account"),
        db_comment="The total number of media items posted by this Instagram account",
    )
    profile_picture_url = models.CharField(
        _("Profile Picture URL"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("URL of the profile picture"),
        db_comment="The URL of the profile picture of the Instagram account",
    )
    website = models.CharField(
        _("Website"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Website associated with the account"),
        db_comment="The website linked in the Instagram account",
    )
    biography = models.TextField(
        _("Biography"),
        null=True,
        blank=True,
        help_text=_("Biography of the account"),
        db_comment="The biography or bio of the Instagram account",
    )
    

    def __repr__(self):
        return f"<InstagramAccount(account_id={self.account_id}, username={self.username})>"

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Instagram Account")
        verbose_name_plural = _("Instagram Accounts")
