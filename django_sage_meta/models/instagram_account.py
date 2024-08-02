from django.db import models
from django.utils.translation import gettext_lazy as _
from django_sage_meta.helper.mixins import AdditionalDataMixin


class InstagramAccount(AdditionalDataMixin):
    """Model representing an Instagram account.

    Attributes:
        account_id (str): The unique identifier for the account.
        username (str): The username of the account.
        follows_count (int): The number of accounts this account follows.
        followers_count (int): The number of followers of this account.
        media_count (int): The number of media items posted by this account.
        profile_picture_url (str): The URL of the profile picture.
        website (str): The website associated with the account.
        biography (str): The biography of the account.
        media (list): The list of media items posted by this account.
        insights (list): The list of insights for this account.
        stories (list): The list of stories posted by this account.

    """

    account_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Account ID"),
        help_text=_("Unique identifier for the account"),
        db_comment="Primary key for the Instagram account",
    )
    username = models.CharField(
        max_length=255,
        verbose_name=_("Username"),
        help_text=_("Username of the account"),
        db_comment="The handle or username of the Instagram account",
    )
    follows_count = models.IntegerField(
        verbose_name=_("Follows Count"),
        help_text=_("Number of accounts this account follows"),
        db_comment="The total number of accounts followed by this Instagram account",
    )
    followers_count = models.IntegerField(
        verbose_name=_("Followers Count"),
        help_text=_("Number of followers of this account"),
        db_comment="The total number of followers of this Instagram account",
    )

    media_count = models.IntegerField(
        verbose_name=_("Media Count"),
        help_text=_("Number of media items posted by this account"),
        db_comment="The total number of media items posted by this Instagram account",
    )
    profile_picture_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Profile Picture URL"),
        help_text=_("URL of the profile picture"),
        db_comment="The URL of the profile picture of the Instagram account",
    )
    website = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Website"),
        help_text=_("Website associated with the account"),
        db_comment="The website linked in the Instagram account",
    )
    biography = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Biography"),
        help_text=_("Biography of the account"),
        db_comment="The biography or bio of the Instagram account",
    )
    media = models.ManyToManyField(
        "Media",
        blank=True,
        verbose_name=_("Media"),
        help_text=_("List of media items posted by this account"),
        db_comment="Media items posted by this Instagram account",
        related_name="instagram_accounts",
    )
    insights = models.ManyToManyField(
        "Insight",
        blank=True,
        verbose_name=_("Insights"),
        help_text=_("List of insights for this account"),
        db_comment="Insights related to the Instagram account",
        related_name="instagram_accounts",
    )
    stories = models.ManyToManyField(
        "Story",
        blank=True,
        verbose_name=_("Stories"),
        help_text=_("List of stories posted by this account"),
        db_comment="Stories posted by this Instagram account",
        related_name="instagram_accounts",
    )

    def __repr__(self):
        return f"<InstagramAccount(account_id={self.account_id}, username={self.username})>"

    def __str__(self):
        return self.username
