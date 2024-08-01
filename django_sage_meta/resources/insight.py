from import_export import resources
from ..models import Insight


class InsightResource(resources.ModelResource):
    class Meta:
        model = Insight
