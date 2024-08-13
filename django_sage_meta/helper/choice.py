from django.db import models


class ContentFileEnum(models.TextChoices):
    image = ("image", "IMAGE")
    videos = ("videos", "VIDEOS")


class InsightKindEnum(models.TextChoices):
    account = ("account", "ACCOUNT")
    media = ("media", "MEDIA")
