from django.contrib import admin
from ..models import CommentPublisher
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .actions.comment_publish import puth_comment

@admin.register(CommentPublisher)
class CommentPublishAdmin(admin.ModelAdmin):
    actions=[puth_comment]

