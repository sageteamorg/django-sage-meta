from django.db import models


class ContentFileEnum(models.TextChoices):
    reels = ("reels", "REELS")
    post = ("post", "POST")
