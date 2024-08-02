from django.contrib import admin
from django_sage_meta.models import CommentPublisher


@admin.register(CommentPublisher)
class CommentPublishAdmin(admin.ModelAdmin):
    list_display=[
        "user",
        "media"
    ]
