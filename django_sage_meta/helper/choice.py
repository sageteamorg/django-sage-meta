from django.db import models


class ContentFileEnum(models.TextChoices):
    image = ("image", "IMAGE")
    videos = ("videos", "VIDEOS")

