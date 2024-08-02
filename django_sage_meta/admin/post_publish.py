from django_sage_meta.models import PostPublisher
from django.contrib import admin
from django_sage_meta.admin.actions.post_publish import puth_post


@admin.register(PostPublisher)
class PostPublishAdmin(admin.ModelAdmin):
    actions = [puth_post]
