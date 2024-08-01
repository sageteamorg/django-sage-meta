from import_export import resources
from ..models import InstagramAccount


class InstagramAccountResource(resources.ModelResource):
    class Meta:
        model = InstagramAccount
