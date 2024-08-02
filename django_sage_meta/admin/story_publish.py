from ..models import StoryPublisher
from django.contrib import admin
from django_sage_meta.admin.actions.publish_story import puth_story


@admin.register(StoryPublisher)
class StoryPublisherAdmin(admin.ModelAdmin):
    actions = [puth_story]
