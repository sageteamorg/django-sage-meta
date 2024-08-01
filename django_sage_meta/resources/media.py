from import_export import resources
from ..models import Media


class MediaResource(resources.ModelResource):
    class Meta:
        model = Media
