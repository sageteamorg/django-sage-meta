from ..models import StoryPublisher
from django.contrib import admin
from .actions.publish_story import puth_story

@admin.register(StoryPublisher)
class StoryPublisherAdmin(admin.ModelAdmin):
    actions=[puth_story]
