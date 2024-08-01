from import_export import resources
from ..models import FacebookPageData


class FacebookPageDataResource(resources.ModelResource):
    class Meta:
        model = FacebookPageData
