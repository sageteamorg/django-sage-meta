from django_sage_meta.models import PostPublisher
from django.contrib import admin


@admin.register(PostPublisher)
class PostPublishAdmin(admin.ModelAdmin):
    list_display=[
        "caption"
    ]
