from ..models import StoryPublisher
from django.contrib import admin

@admin.register(StoryPublisher)
class StoryPublisherAdmin(admin.ModelAdmin):
    list_display=[
        "file_url",
        "kind"
    ]
