from import_export import resources
from ..models import Story


class StoryResource(resources.ModelResource):
    class Meta:
        model = Story
