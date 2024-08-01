from django.contrib import admin
from django_sage_meta.models import CommentPublisher
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_sage_meta.admin.actions.comment_publish import puth_comment

@admin.register(CommentPublisher)
class CommentPublishAdmin(admin.ModelAdmin):
    actions=[puth_comment]

