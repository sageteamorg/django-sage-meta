from ..models import PostPublisher
from django.contrib import admin
from .actions.post_publish import puth_post

@admin.register(PostPublisher)
class PostPublishAdmin(admin.ModelAdmin):
    actions=[puth_post]
